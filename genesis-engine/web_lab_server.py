#!/usr/bin/env python3
"""
Chemistry Lab Web Server
A lightweight HTTP server with API endpoints for the molecular chemistry laboratory.
Serves static files and provides REST API access to the chemical registry.
"""

import http.server
import socketserver
import json
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any

# Import our molecular chemistry components
try:
    from .connectors.chemical_registry import ChemicalRegistry, SearchQuery
except ImportError:
    from connectors.chemical_registry import ChemicalRegistry


class ChemistryLabHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with API endpoints for the chemistry lab"""

    def __init__(self, *args, chemical_registry=None, **kwargs):
        self.chemical_registry = chemical_registry or ChemicalRegistry()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests for both static files and API endpoints"""
        parsed_path = urlparse(self.path)

        if parsed_path.path.startswith("/api/"):
            self._handle_api_request(parsed_path)
        else:
            # Serve static files (HTML, CSS, JS, etc.)
            super().do_GET()

    def _handle_api_request(self, parsed_path):
        """Handle API requests"""
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        try:
            if path == "/api/molecules":
                self._handle_molecules_api(query_params)
            elif path == "/api/molecules/count":
                self._handle_molecules_count_api()
            elif path.startswith("/api/molecules/") and path.endswith("/svg"):
                # Handle SVG request: /api/molecules/{name}/svg
                molecule_name = path.split("/")[-2]
                self._handle_molecule_svg_api(molecule_name)
            elif path.startswith("/api/molecules/"):
                # Handle specific molecule by ID
                molecule_id = path.split("/")[-1]
                self._handle_molecule_detail_api(molecule_id)
            else:
                self._send_error_response(404, "API endpoint not found")

        except Exception as e:
            print(f"❌ API Error: {e}")
            self._send_error_response(500, f"Internal server error: {str(e)}")

    def _handle_molecules_api(self, query_params):
        """Handle /api/molecules - return all registered molecules"""
        try:
            # Parse query parameters
            limit = int(query_params.get("limit", [50])[0])
            offset = int(query_params.get("offset", [0])[0])
            order_by = query_params.get("order_by", ["creation_date DESC"])[0]

            print(f"🔍 API request: /api/molecules (limit={limit}, offset={offset})")

            # Get molecules from registry
            components = self.chemical_registry.get_all_components(
                limit=limit, offset=offset, order_by=order_by
            )
            total_count = self.chemical_registry.get_component_count()

            print(f"📊 Retrieved {len(components)} components (total: {total_count})")

            # Convert to JSON-serializable format
            molecules_data = []
            for comp in components:
                try:
                    molecules_data.append(
                        {
                            "name": comp.name,
                            "molecular_formula": comp.molecular_formula,
                            "element_composition": comp.element_composition,
                            "stability": comp.stability.value,
                            "bond_energy": comp.bond_energy,
                            "creation_date": comp.creation_date.isoformat()
                            if comp.creation_date
                            else None,
                            "created_by": comp.created_by,
                            "version": comp.version,
                            "description": comp.description,
                            "usage_count": comp.usage_count,
                            "last_used": comp.last_used.isoformat()
                            if comp.last_used
                            else None,
                            "properties": comp.properties,
                        }
                    )
                except Exception as e:
                    print(f"⚠️ Error serializing component {comp.name}: {e}")
                    continue

            response_data = {
                "molecules": molecules_data,
                "total_count": total_count,
                "limit": limit,
                "offset": offset,
                "returned_count": len(molecules_data),
            }

            print(f"✅ Sending {len(molecules_data)} molecules in response")
            self._send_json_response(response_data)

        except Exception as e:
            print(f"❌ Error in molecules API: {e}")
            self._send_error_response(500, f"Failed to retrieve molecules: {str(e)}")

    def _handle_molecules_count_api(self):
        """Handle /api/molecules/count - return total molecule count"""
        try:
            count = self.chemical_registry.get_component_count()
            self._send_json_response({"count": count})
        except Exception as e:
            print(f"❌ Error in molecules count API: {e}")
            self._send_error_response(500, f"Failed to get molecule count: {str(e)}")

    def _handle_molecule_svg_api(self, molecule_name):
        """Handle /api/molecules/{name}/svg - return SVG visualization"""
        try:
            print(f"🎨 SVG request for molecule: {molecule_name}")

            # Calculate path to SVG file
            # Use the same project root logic
            if os.path.basename(os.getcwd()) == "web_lab":
                # We're in web_lab, so project root is parent directory
                project_root = Path(os.getcwd()).parent
            else:
                project_root = Path(os.getcwd())

            svg_path = (
                project_root / "hive" / "components" / molecule_name / "honeyprint.svg"
            )

            print(f"🔍 Looking for SVG at: {svg_path}")

            if not svg_path.exists():
                print(f"❌ SVG file not found: {svg_path}")
                self._send_error_response(
                    404, f"SVG not found for molecule: {molecule_name}"
                )
                return

            # Read SVG content
            with open(svg_path, "r", encoding="utf-8") as f:
                svg_content = f.read()

            print(f"✅ SVG loaded successfully ({len(svg_content)} chars)")

            # Send SVG response
            self.send_response(200)
            self.send_header("Content-type", "image/svg+xml")
            self.send_header("Access-Control-Allow-Origin", "*")  # Enable CORS
            self.send_header(
                "Cache-Control", "public, max-age=3600"
            )  # Cache for 1 hour
            self.end_headers()

            self.wfile.write(svg_content.encode("utf-8"))

        except Exception as e:
            print(f"❌ Error serving SVG for {molecule_name}: {e}")
            self._send_error_response(500, f"Failed to load SVG: {str(e)}")

    def _handle_molecule_detail_api(self, molecule_id):
        """Handle /api/molecules/{id} - return specific molecule details"""
        component = self.chemical_registry.get_component(molecule_id)

        if not component:
            self._send_error_response(404, "Molecule not found")
            return

        molecule_data = {
            "name": component.name,
            "molecular_formula": component.molecular_formula,
            "element_composition": component.element_composition,
            "stability": component.stability.value,
            "bond_energy": component.bond_energy,
            "creation_date": component.creation_date.isoformat()
            if component.creation_date
            else None,
            "created_by": component.created_by,
            "version": component.version,
            "description": component.description,
            "usage_count": component.usage_count,
            "last_used": component.last_used.isoformat()
            if component.last_used
            else None,
            "properties": component.properties,
            "similar_components": component.similar_components,
            "isotopes": component.isotopes,
            "reaction_products": component.reaction_products,
            "decomposition_products": component.decomposition_products,
        }

        self._send_json_response(molecule_data)

    def _send_json_response(self, data: Dict[str, Any]):
        """Send a JSON response"""
        json_data = json.dumps(data, indent=2, default=str)

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")  # Enable CORS
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

        self.wfile.write(json_data.encode("utf-8"))

    def _send_error_response(self, status_code: int, message: str):
        """Send an error response"""
        error_data = {"error": message, "status_code": status_code}

        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")  # Enable CORS
        self.end_headers()

        json_data = json.dumps(error_data)
        self.wfile.write(json_data.encode("utf-8"))

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def start_chemistry_lab_server(port: int, web_lab_dir: Path):
    """Start the chemistry lab web server with API endpoints"""
    # Calculate absolute path to database before changing directories
    # Go up from genesis-engine directory if we're running from there
    if os.path.basename(os.getcwd()) == "genesis-engine":
        project_root = os.path.dirname(os.getcwd())
    else:
        project_root = os.getcwd()

    db_path = os.path.join(project_root, "chemical_registry.db")

    # Change to web lab directory to serve static files
    os.chdir(web_lab_dir)

    try:
        # Initialize chemical registry with absolute path
        print(f"🔗 Using database: {db_path}")
        chemical_registry = ChemicalRegistry(db_path)

        # Test database connection and log component count
        try:
            component_count = chemical_registry.get_component_count()
            print(f"📊 Database connected: {component_count} molecules available")

            if component_count > 0:
                # Show sample molecules for verification
                sample_components = chemical_registry.get_all_components(limit=3)
                print("🧬 Sample molecules:")
                for comp in sample_components:
                    print(
                        f"   • {comp.name}: {comp.molecular_formula} ({comp.stability.value})"
                    )
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            print("⚠️ API will return empty results")

        # Create handler with registry
        def create_handler(*args, **kwargs):
            return ChemistryLabHandler(
                *args, chemical_registry=chemical_registry, **kwargs
            )

        # Start server
        with socketserver.TCPServer(("", port), create_handler) as httpd:
            print(f"🧪 Chemistry Lab Server running on port {port}")
            print("📊 API endpoints available:")
            print("   GET /api/molecules - List all registered molecules")
            print("   GET /api/molecules/count - Get total molecule count")
            print("   GET /api/molecules/{id} - Get specific molecule details")
            print(f"🌐 Web interface: http://localhost:{port}/chemistry_lab.html")

            httpd.serve_forever()

    finally:
        # Restore original directory
        os.chdir(original_cwd)


if __name__ == "__main__":
    # Test server directly
    from pathlib import Path

    web_dir = Path(__file__).parent.parent / "web_lab"
    start_chemistry_lab_server(8000, web_dir)
