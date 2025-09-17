#!/usr/bin/env python3
"""
🎮⚡ INTERACTIVE EVOLUTION CONSOLE ⚡🎮
Real-time Control Interface for Self-Evolving Code

This console provides direct control over the evolution process, allowing users to:
- Guide evolutionary direction in real-time
- Inject custom fitness criteria
- Control mutation rates and strategies
- Monitor evolution in real-time
- Save and load evolution states

Author: Quantum Hive Collective
Version: 1.0.0 - Interactive Evolution
"""

import asyncio
import json
import time
import random
import sys
import os
import cmd
import threading
from datetime import datetime
from typing import Dict, List, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid
import signal

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from dna_core.royal_jelly.quantum_dna_genetic_programming import (
        QuantumDNAGeneticProgramming,
        CodeGene,
        CodeChromosome,
        EvolvingComponent,
        EvolutionMetrics,
    )
    from demonstrations.quantum_evolution_orchestrator import (
        QuantumEvolutionOrchestrator,
    )
    from demonstrations.live_evolution_showcase import (
        LiveEvolutionShowcase,
        VisualizationMode,
    )
    from demonstrations.enterprise_scenario_simulator import EnterpriseScenarioSimulator
except ImportError as e:
    print(f"⚠️  Import warning: {e}")
    print("Running in standalone mode...")


class EvolutionCommand(Enum):
    """Available evolution control commands"""

    START = "start"
    STOP = "stop"
    PAUSE = "pause"
    RESUME = "resume"
    ACCELERATE = "accelerate"
    DECELERATE = "decelerate"
    MUTATE = "mutate"
    CROSSOVER = "crossover"
    EVALUATE = "evaluate"
    SAVE_STATE = "save_state"
    LOAD_STATE = "load_state"
    SET_FITNESS = "set_fitness"
    INJECT_CODE = "inject_code"
    VISUALIZE = "visualize"
    STATUS = "status"
    HELP = "help"


class EvolutionState(Enum):
    """Current state of evolution process"""

    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    ACCELERATED = "accelerated"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class ConsoleSession:
    """Interactive console session data"""

    session_id: str
    start_time: datetime
    user_commands: List[Dict[str, Any]] = field(default_factory=list)
    evolution_history: List[Dict[str, Any]] = field(default_factory=list)
    custom_fitness_functions: Dict[str, Callable] = field(default_factory=dict)
    bookmarks: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    settings: Dict[str, Any] = field(default_factory=dict)


class InteractiveEvolutionConsole(cmd.Cmd):
    """Interactive command-line interface for evolution control"""

    intro = """
🧬✨ QUANTUM HIVE INTERACTIVE EVOLUTION CONSOLE ✨🧬

Welcome to the future of software development!
Control the evolution of code in real-time through this interactive console.

Type 'help' for available commands, or 'quick_start' to begin evolution.
Type 'exit' or 'quit' to close the console.
    """

    prompt = "🧬 QuantumHive> "

    def __init__(self):
        super().__init__()
        self.session = ConsoleSession(
            session_id=str(uuid.uuid4()),
            start_time=datetime.now(),
            settings={
                "mutation_rate": 0.1,
                "crossover_rate": 0.7,
                "population_size": 50,
                "max_generations": 100,
                "visualization_mode": "terminal_matrix",
                "auto_save": True,
                "evolution_speed": 1.0,
            },
        )

        self.evolution_state = EvolutionState.IDLE
        self.genetic_engine = None
        self.orchestrator = None
        self.showcase = None
        self.scenario_simulator = None

        self.current_generation = 0
        self.current_population = []
        self.evolution_task = None
        self.visualization_task = None

        # Background monitoring
        self.monitor_active = False
        self.monitor_thread = None

        # Command history
        self.command_history = []

        # Initialize components
        asyncio.create_task(self.initialize_components())

    async def initialize_components(self):
        """Initialize all quantum hive components"""
        try:
            print("🔧 Initializing Quantum Hive components...")

            # Initialize genetic programming engine
            self.genetic_engine = QuantumDNAGeneticProgramming()

            # Initialize orchestrator
            self.orchestrator = QuantumEvolutionOrchestrator()
            await self.orchestrator.initialize()

            # Initialize showcase
            self.showcase = LiveEvolutionShowcase()
            await self.showcase.initialize()

            # Initialize scenario simulator
            self.scenario_simulator = EnterpriseScenarioSimulator()
            await self.scenario_simulator.initialize()

            print("✅ All components initialized successfully!")

        except Exception as e:
            print(f"⚠️  Component initialization warning: {e}")
            print("🎯 Running in demo mode with limited functionality")

    def do_quick_start(self, args):
        """Start evolution with default parameters"""
        print("🚀 Quick Start - Initializing evolution with default parameters...")
        self._set_default_population()
        self.do_start("")

    def do_start(self, args):
        """Start the evolution process
        Usage: start [population_size] [generations]
        Example: start 100 50
        """
        if self.evolution_state == EvolutionState.RUNNING:
            print("⚠️  Evolution already running! Use 'pause' or 'stop' first.")
            return

        # Parse arguments
        params = args.split() if args else []
        population_size = (
            int(params[0])
            if len(params) > 0
            else self.session.settings["population_size"]
        )
        max_generations = (
            int(params[1])
            if len(params) > 1
            else self.session.settings["max_generations"]
        )

        print("🧬 Starting evolution...")
        print(f"   Population Size: {population_size}")
        print(f"   Max Generations: {max_generations}")
        print(f"   Mutation Rate: {self.session.settings['mutation_rate']}")
        print(f"   Crossover Rate: {self.session.settings['crossover_rate']}")

        self.evolution_state = EvolutionState.RUNNING
        self.current_generation = 0

        # Start evolution in background
        self.evolution_task = asyncio.create_task(
            self._run_evolution_loop(population_size, max_generations)
        )

        # Start monitoring
        self._start_monitoring()

        self._log_command(
            "start",
            {"population_size": population_size, "max_generations": max_generations},
        )

    def do_stop(self, args):
        """Stop the evolution process"""
        if self.evolution_state == EvolutionState.IDLE:
            print("⚠️  Evolution not running.")
            return

        print("🛑 Stopping evolution...")
        self.evolution_state = EvolutionState.STOPPED

        if self.evolution_task:
            self.evolution_task.cancel()

        self._stop_monitoring()

        print("✅ Evolution stopped successfully.")
        self._log_command("stop", {})

    def do_pause(self, args):
        """Pause the evolution process"""
        if self.evolution_state != EvolutionState.RUNNING:
            print("⚠️  Evolution not running.")
            return

        print("⏸️  Pausing evolution...")
        self.evolution_state = EvolutionState.PAUSED
        self._log_command("pause", {})

    def do_resume(self, args):
        """Resume the evolution process"""
        if self.evolution_state != EvolutionState.PAUSED:
            print("⚠️  Evolution not paused.")
            return

        print("▶️  Resuming evolution...")
        self.evolution_state = EvolutionState.RUNNING
        self._log_command("resume", {})

    def do_accelerate(self, args):
        """Accelerate evolution speed
        Usage: accelerate [factor]
        Example: accelerate 2.5
        """
        factor = float(args) if args else 2.0
        self.session.settings["evolution_speed"] *= factor

        print(f"⚡ Evolution accelerated by {factor}x")
        print(f"   Current speed: {self.session.settings['evolution_speed']:.1f}x")

        self._log_command("accelerate", {"factor": factor})

    def do_decelerate(self, args):
        """Decelerate evolution speed
        Usage: decelerate [factor]
        Example: decelerate 2.0
        """
        factor = float(args) if args else 2.0
        self.session.settings["evolution_speed"] /= factor

        print(f"🐌 Evolution decelerated by {factor}x")
        print(f"   Current speed: {self.session.settings['evolution_speed']:.1f}x")

        self._log_command("decelerate", {"factor": factor})

    def do_mutate(self, args):
        """Trigger manual mutation
        Usage: mutate [component_id] [mutation_type]
        Example: mutate comp_001 point_mutation
        """
        params = args.split() if args else []
        component_id = params[0] if len(params) > 0 else "random"
        mutation_type = params[1] if len(params) > 1 else "random"

        print("🧬 Triggering manual mutation...")
        print(f"   Target: {component_id}")
        print(f"   Type: {mutation_type}")

        # Simulate mutation effect
        success = random.random() > 0.2  # 80% success rate
        if success:
            fitness_change = random.uniform(-0.1, 0.3)
            print(f"✅ Mutation successful! Fitness change: {fitness_change:+.3f}")
        else:
            print("❌ Mutation failed - component remained stable")

        self._log_command(
            "mutate",
            {
                "component_id": component_id,
                "mutation_type": mutation_type,
                "success": success,
            },
        )

    def do_crossover(self, args):
        """Trigger manual crossover between components
        Usage: crossover [parent1] [parent2]
        Example: crossover comp_001 comp_002
        """
        params = args.split() if args else []
        parent1 = params[0] if len(params) > 0 else "random"
        parent2 = params[1] if len(params) > 1 else "random"

        print("🔗 Triggering crossover...")
        print(f"   Parent 1: {parent1}")
        print(f"   Parent 2: {parent2}")

        # Simulate crossover
        child_fitness = random.uniform(0.4, 0.9)
        print(f"✅ Crossover successful! New offspring fitness: {child_fitness:.3f}")

        self._log_command(
            "crossover",
            {"parent1": parent1, "parent2": parent2, "child_fitness": child_fitness},
        )

    def do_set_fitness(self, args):
        """Set custom fitness function
        Usage: set_fitness [function_name] [expression]
        Example: set_fitness performance "lambda x: x.speed * x.accuracy"
        """
        params = args.split(" ", 1) if args else []
        if len(params) < 2:
            print("Usage: set_fitness [function_name] [expression]")
            return

        func_name = params[0]
        expression = params[1]

        try:
            # Create custom fitness function (simplified for demo)
            custom_func = eval(expression)
            self.session.custom_fitness_functions[func_name] = custom_func

            print(f"✅ Custom fitness function '{func_name}' created")
            print(f"   Expression: {expression}")

        except Exception as e:
            print(f"❌ Failed to create fitness function: {e}")

        self._log_command(
            "set_fitness", {"function_name": func_name, "expression": expression}
        )

    def do_inject_code(self, args):
        """Inject custom code into evolution
        Usage: inject_code [component_name] [code_snippet]
        """
        params = args.split(" ", 1) if args else []
        if len(params) < 2:
            print("Usage: inject_code [component_name] [code_snippet]")
            return

        component_name = params[0]
        code_snippet = params[1]

        print("💉 Injecting custom code...")
        print(f"   Target: {component_name}")
        print(f"   Code: {code_snippet[:50]}{'...' if len(code_snippet) > 50 else ''}")

        # Simulate code injection
        fitness_impact = random.uniform(-0.2, 0.4)
        print(f"✅ Code injected! Fitness impact: {fitness_impact:+.3f}")

        self._log_command(
            "inject_code",
            {"component_name": component_name, "code_length": len(code_snippet)},
        )

    def do_visualize(self, args):
        """Start visualization mode
        Usage: visualize [mode] [duration]
        Available modes: matrix, dna_helix, consciousness_tree, quantum_field, enterprise_dashboard
        Example: visualize matrix 60
        """
        params = args.split() if args else []
        mode = params[0] if len(params) > 0 else "matrix"
        duration = int(params[1]) if len(params) > 1 else 30

        # Map mode names to enum values
        mode_map = {
            "matrix": VisualizationMode.TERMINAL_MATRIX,
            "dna_helix": VisualizationMode.DNA_HELIX_VIEW,
            "consciousness_tree": VisualizationMode.CONSCIOUSNESS_TREE,
            "quantum_field": VisualizationMode.QUANTUM_FIELD,
            "enterprise_dashboard": VisualizationMode.ENTERPRISE_DASHBOARD,
        }

        vis_mode = mode_map.get(mode, VisualizationMode.TERMINAL_MATRIX)

        print("🎬 Starting visualization...")
        print(f"   Mode: {vis_mode.value}")
        print(f"   Duration: {duration} seconds")
        print("   Press Ctrl+C to stop early")

        if self.showcase:
            self.visualization_task = asyncio.create_task(
                self.showcase.start_live_showcase(
                    vis_mode, duration_minutes=duration / 60
                )
            )
        else:
            print("⚠️  Showcase not available - running demo visualization")
            self._run_demo_visualization(mode, duration)

        self._log_command("visualize", {"mode": mode, "duration": duration})

    def do_status(self, args):
        """Display current evolution status"""
        print("\n📊 EVOLUTION STATUS REPORT")
        print(f"{'=' * 50}")
        print(f"State: {self.evolution_state.value.upper()}")
        print(f"Session ID: {self.session.session_id}")
        print(f"Runtime: {str(datetime.now() - self.session.start_time).split('.')[0]}")
        print(f"Current Generation: {self.current_generation}")

        print("\n⚙️  SETTINGS:")
        for key, value in self.session.settings.items():
            print(f"   {key}: {value}")

        print("\n🧬 POPULATION:")
        print(f"   Size: {len(self.current_population)}")
        if self.current_population:
            avg_fitness = sum(
                comp.get("fitness", 0) for comp in self.current_population
            ) / len(self.current_population)
            print(f"   Average Fitness: {avg_fitness:.3f}")
            best_fitness = max(
                comp.get("fitness", 0) for comp in self.current_population
            )
            print(f"   Best Fitness: {best_fitness:.3f}")

        print("\n📈 SESSION STATISTICS:")
        print(f"   Commands Executed: {len(self.session.user_commands)}")
        print(f"   Evolution Events: {len(self.session.evolution_history)}")
        print(
            f"   Custom Fitness Functions: {len(self.session.custom_fitness_functions)}"
        )
        print(f"   Bookmarks: {len(self.session.bookmarks)}")

        self._log_command("status", {})

    def do_save_state(self, args):
        """Save current evolution state
        Usage: save_state [filename]
        Example: save_state my_evolution
        """
        filename = (
            args.strip()
            if args
            else f"evolution_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        filepath = f"/tmp/{filename}.json"

        state_data = {
            "session": {
                "session_id": self.session.session_id,
                "start_time": self.session.start_time.isoformat(),
                "settings": self.session.settings,
            },
            "evolution": {
                "state": self.evolution_state.value,
                "generation": self.current_generation,
                "population": self.current_population,
            },
            "history": self.session.evolution_history[-50:],  # Last 50 events
        }

        try:
            with open(filepath, "w") as f:
                json.dump(state_data, f, indent=2)

            print(f"💾 Evolution state saved to: {filepath}")

        except Exception as e:
            print(f"❌ Failed to save state: {e}")

        self._log_command("save_state", {"filename": filename})

    def do_load_state(self, args):
        """Load saved evolution state
        Usage: load_state [filename]
        Example: load_state my_evolution
        """
        if not args:
            print("Usage: load_state [filename]")
            return

        filename = args.strip()
        filepath = f"/tmp/{filename}.json"

        try:
            with open(filepath, "r") as f:
                state_data = json.load(f)

            # Restore session settings
            self.session.settings.update(state_data["session"]["settings"])

            # Restore evolution state
            self.evolution_state = EvolutionState(state_data["evolution"]["state"])
            self.current_generation = state_data["evolution"]["generation"]
            self.current_population = state_data["evolution"]["population"]

            print(f"📂 Evolution state loaded from: {filepath}")
            print(f"   Restored generation: {self.current_generation}")
            print(f"   Population size: {len(self.current_population)}")

        except Exception as e:
            print(f"❌ Failed to load state: {e}")

        self._log_command("load_state", {"filename": filename})

    def do_bookmark(self, args):
        """Create bookmark for current state
        Usage: bookmark [name] [description]
        Example: bookmark best_run "High performance evolution"
        """
        params = args.split(" ", 1) if args else []
        name = (
            params[0] if len(params) > 0 else f"bookmark_{len(self.session.bookmarks)}"
        )
        description = params[1] if len(params) > 1 else "Auto-generated bookmark"

        bookmark = {
            "name": name,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "generation": self.current_generation,
            "state": self.evolution_state.value,
            "settings": self.session.settings.copy(),
        }

        self.session.bookmarks[name] = bookmark

        print(f"🔖 Bookmark '{name}' created")
        print(f"   Description: {description}")
        print(f"   Generation: {self.current_generation}")

        self._log_command("bookmark", {"name": name, "description": description})

    def do_list_bookmarks(self, args):
        """List all bookmarks"""
        if not self.session.bookmarks:
            print("📝 No bookmarks created yet. Use 'bookmark' command to create one.")
            return

        print(f"\n🔖 BOOKMARKS ({len(self.session.bookmarks)})")
        print(f"{'=' * 60}")

        for name, bookmark in self.session.bookmarks.items():
            print(f"📌 {name}")
            print(f"   Description: {bookmark['description']}")
            print(f"   Generation: {bookmark['generation']}")
            print(f"   Time: {bookmark['timestamp']}")
            print()

    def do_scenario(self, args):
        """Run enterprise scenario simulation
        Usage: scenario [scenario_id]
        Available: ecom_recommendation_engine, fintech_fraud_detection, manufacturing_predictive_maintenance
        """
        if not args:
            print("Available scenarios:")
            scenarios = [
                "ecom_recommendation_engine",
                "fintech_fraud_detection",
                "manufacturing_predictive_maintenance",
                "retail_inventory_optimization",
            ]
            for scenario in scenarios:
                print(f"   • {scenario}")
            return

        scenario_id = args.strip()

        print(f"🏢 Starting enterprise scenario: {scenario_id}")

        if self.scenario_simulator:
            asyncio.create_task(
                self.scenario_simulator.run_scenario_simulation(
                    scenario_id, accelerated=True
                )
            )
        else:
            print("⚠️  Scenario simulator not available")

        self._log_command("scenario", {"scenario_id": scenario_id})

    def do_settings(self, args):
        """View or modify settings
        Usage: settings [key] [value]
        Example: settings mutation_rate 0.2
        """
        params = args.split() if args else []

        if not params:
            # Display all settings
            print("\n⚙️  CURRENT SETTINGS")
            print(f"{'=' * 40}")
            for key, value in self.session.settings.items():
                print(f"{key}: {value}")
            return

        if len(params) == 1:
            # Display specific setting
            key = params[0]
            if key in self.session.settings:
                print(f"{key}: {self.session.settings[key]}")
            else:
                print(f"❌ Unknown setting: {key}")
            return

        # Modify setting
        key, value = params[0], params[1]

        # Convert value to appropriate type
        try:
            if value.lower() in ["true", "false"]:
                value = value.lower() == "true"
            elif "." in value:
                value = float(value)
            elif value.isdigit():
                value = int(value)
        except:
            pass  # Keep as string

        self.session.settings[key] = value
        print(f"✅ Setting updated: {key} = {value}")

        self._log_command("settings", {"key": key, "value": value})

    def do_history(self, args):
        """Display command history
        Usage: history [count]
        Example: history 10
        """
        count = int(args) if args.isdigit() else 20
        recent_commands = self.session.user_commands[-count:]

        print(f"\n📜 COMMAND HISTORY (Last {len(recent_commands)})")
        print(f"{'=' * 50}")

        for i, cmd in enumerate(recent_commands, 1):
            timestamp = cmd["timestamp"][:19]  # Remove microseconds
            print(f"{i:2d}. [{timestamp}] {cmd['command']} {cmd.get('args', '')}")

    def do_exit(self, args):
        """Exit the console"""
        return self.do_quit(args)

    def do_quit(self, args):
        """Quit the console"""
        print("\n👋 Shutting down Quantum Hive Console...")

        # Stop any running tasks
        if self.evolution_task and not self.evolution_task.done():
            self.evolution_task.cancel()

        if self.visualization_task and not self.visualization_task.done():
            self.visualization_task.cancel()

        self._stop_monitoring()

        # Save session summary
        session_summary = {
            "session_id": self.session.session_id,
            "duration": str(datetime.now() - self.session.start_time),
            "commands_executed": len(self.session.user_commands),
            "evolution_events": len(self.session.evolution_history),
            "final_generation": self.current_generation,
        }

        print("📊 Session Summary:")
        print(f"   Duration: {session_summary['duration'].split('.')[0]}")
        print(f"   Commands: {session_summary['commands_executed']}")
        print(f"   Generation: {session_summary['final_generation']}")

        print("\n✨ Thank you for using Quantum Hive! Evolution continues... ✨")
        return True

    def _set_default_population(self):
        """Create default population for quick start"""
        self.current_population = []
        population_size = self.session.settings["population_size"]

        for i in range(population_size):
            component = {
                "id": f"comp_{i:03d}",
                "name": f"Component_{i}",
                "fitness": random.uniform(0.1, 0.8),
                "generation": 0,
                "mutations": 0,
            }
            self.current_population.append(component)

        print(f"🧬 Created default population of {population_size} components")

    async def _run_evolution_loop(self, population_size: int, max_generations: int):
        """Main evolution loop running in background"""
        try:
            while (
                self.evolution_state in [EvolutionState.RUNNING, EvolutionState.PAUSED]
                and self.current_generation < max_generations
            ):
                if self.evolution_state == EvolutionState.PAUSED:
                    await asyncio.sleep(0.5)
                    continue

                # Evolution step
                await self._evolution_step()

                # Respect evolution speed setting
                sleep_time = 1.0 / self.session.settings["evolution_speed"]
                await asyncio.sleep(sleep_time)

        except asyncio.CancelledError:
            print("🛑 Evolution loop cancelled")
        except Exception as e:
            print(f"❌ Evolution loop error: {e}")
            self.evolution_state = EvolutionState.ERROR

    async def _evolution_step(self):
        """Single evolution step"""
        self.current_generation += 1

        # Simulate evolution effects
        for component in self.current_population:
            if random.random() < self.session.settings["mutation_rate"]:
                # Mutation
                fitness_change = random.uniform(-0.1, 0.2)
                component["fitness"] = max(
                    0.0, min(1.0, component["fitness"] + fitness_change)
                )
                component["mutations"] += 1

        # Log evolution event
        event = {
            "timestamp": datetime.now().isoformat(),
            "generation": self.current_generation,
            "type": "generation_advance",
            "population_size": len(self.current_population),
            "avg_fitness": sum(c["fitness"] for c in self.current_population)
            / len(self.current_population),
        }
        self.session.evolution_history.append(event)

    def _start_monitoring(self):
        """Start background monitoring"""
        if not self.monitor_active:
            self.monitor_active = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop, daemon=True
            )
            self.monitor_thread.start()

    def _stop_monitoring(self):
        """Stop background monitoring"""
        self.monitor_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)

    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.monitor_active:
            if self.evolution_state == EvolutionState.RUNNING:
                # Could add real-time monitoring here
                pass
            time.sleep(2)

    def _run_demo_visualization(self, mode: str, duration: int):
        """Run demo visualization when showcase not available"""
        print(f"🎬 Demo visualization: {mode}")
        for i in range(duration):
            if i % 5 == 0:
                print(f"   Evolution frame {i // 5 + 1}: Fitness improving...")
            time.sleep(1)
        print("✅ Visualization complete")

    def _log_command(self, command: str, params: Dict[str, Any]):
        """Log user command"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "parameters": params,
            "generation": self.current_generation,
            "state": self.evolution_state.value,
        }
        self.session.user_commands.append(log_entry)

    def cmdloop(self, intro=None):
        """Override cmdloop to handle Ctrl+C gracefully"""
        try:
            super().cmdloop(intro)
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted. Use 'quit' to exit properly.")
            self.cmdloop("")


def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n⚠️  Console interrupted. Please use 'quit' to exit properly.")


async def main():
    """Main console entry point"""
    # Set up signal handling
    signal.signal(signal.SIGINT, signal_handler)

    print("🧬⚡ QUANTUM HIVE INTERACTIVE EVOLUTION CONSOLE ⚡🧬")
    print("Initializing quantum evolution control interface...\n")

    # Create and start console
    console = InteractiveEvolutionConsole()

    # Run in asyncio context
    await asyncio.sleep(0.1)  # Allow initialization

    # Start command loop in thread to allow async operations
    import threading

    console_thread = threading.Thread(target=console.cmdloop, daemon=False)
    console_thread.start()

    # Keep async context alive
    try:
        while console_thread.is_alive():
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        print("\n🛑 Console terminating...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(
            "\n👋 Quantum Hive Console terminated. Evolution continues in the background..."
        )
