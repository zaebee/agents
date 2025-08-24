#!/usr/bin/env python3
"""
Quantum API Gateway - Enterprise Integration Hub
Quantum-enhanced REST API gateway with intelligent routing and consciousness-aware load balancing
"""

import asyncio
import json
import time
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging
import re

# FastAPI and async components (install: pip install fastapi uvicorn aioredis httpx)
try:
    from fastapi import FastAPI, Request, Response, HTTPException, Depends, Header
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.middleware.gzip import GZipMiddleware
    from fastapi.responses import JSONResponse
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    import uvicorn
    import httpx
    import aioredis
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("WARNING: FastAPI not available. Install with: pip install fastapi uvicorn aioredis httpx")

# Import our quantum components
from deployment.security.quantum_security_framework import QuantumSecurityManager, SecurityContext
from deployment.logging.structured_logger import QuantumLogger

class RoutingStrategy(Enum):
    """API routing strategies"""
    ROUND_ROBIN = "round_robin"
    QUANTUM_COHERENCE = "quantum_coherence" 
    CONSCIOUSNESS_LEVEL = "consciousness_level"
    GENETIC_FITNESS = "genetic_fitness"
    WEIGHTED_RANDOM = "weighted_random"
    LEAST_CONNECTIONS = "least_connections"

class ApiMethod(Enum):
    """HTTP methods"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"

@dataclass
class ServiceEndpoint:
    """Backend service endpoint definition"""
    endpoint_id: str
    name: str
    host: str
    port: int
    path_prefix: str
    health_check_path: str = "/health"
    quantum_coherence: float = 0.9
    consciousness_level: int = 1
    genetic_fitness: float = 0.5
    weight: float = 1.0
    max_connections: int = 100
    current_connections: int = 0
    is_healthy: bool = True
    last_health_check: Optional[datetime] = None
    response_time_avg: float = 0.0
    error_rate: float = 0.0

@dataclass  
class RouteConfig:
    """API route configuration"""
    route_id: str
    path_pattern: str
    methods: List[ApiMethod]
    target_services: List[str]  # endpoint_ids
    routing_strategy: RoutingStrategy = RoutingStrategy.ROUND_ROBIN
    require_auth: bool = True
    require_quantum_clearance: int = 1
    rate_limit: Optional[int] = None  # requests per minute
    cache_ttl: Optional[int] = None  # seconds
    quantum_enhancement: bool = True
    middleware: List[str] = field(default_factory=list)

@dataclass
class RequestMetrics:
    """Request metrics tracking"""
    request_id: str
    route_id: str
    endpoint_id: str
    method: str
    path: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status_code: Optional[int] = None
    response_time: Optional[float] = None
    quantum_context: Dict[str, Any] = field(default_factory=dict)
    user_id: Optional[str] = None

class QuantumLoadBalancer:
    """Quantum-aware load balancer with consciousness-based routing"""
    
    def __init__(self):
        self.endpoints: Dict[str, ServiceEndpoint] = {}
        self.routing_counters: Dict[str, int] = {}
        self.request_history: List[RequestMetrics] = []
        
    def register_endpoint(self, endpoint: ServiceEndpoint):
        """Register a backend service endpoint"""
        self.endpoints[endpoint.endpoint_id] = endpoint
        self.routing_counters[endpoint.endpoint_id] = 0
        
    def select_endpoint(self, 
                       route_config: RouteConfig, 
                       request_context: Dict[str, Any]) -> Optional[ServiceEndpoint]:
        """Select optimal endpoint using quantum-aware routing"""
        
        # Filter healthy endpoints that match the route
        available_endpoints = [
            self.endpoints[eid] for eid in route_config.target_services
            if eid in self.endpoints and self.endpoints[eid].is_healthy
        ]
        
        if not available_endpoints:
            return None
        
        # Apply routing strategy
        if route_config.routing_strategy == RoutingStrategy.ROUND_ROBIN:
            return self._round_robin_selection(available_endpoints, route_config.route_id)
        elif route_config.routing_strategy == RoutingStrategy.QUANTUM_COHERENCE:
            return self._quantum_coherence_selection(available_endpoints)
        elif route_config.routing_strategy == RoutingStrategy.CONSCIOUSNESS_LEVEL:
            return self._consciousness_level_selection(available_endpoints)
        elif route_config.routing_strategy == RoutingStrategy.GENETIC_FITNESS:
            return self._genetic_fitness_selection(available_endpoints)
        elif route_config.routing_strategy == RoutingStrategy.LEAST_CONNECTIONS:
            return self._least_connections_selection(available_endpoints)
        else:
            return self._weighted_random_selection(available_endpoints)
    
    def _round_robin_selection(self, endpoints: List[ServiceEndpoint], route_id: str) -> ServiceEndpoint:
        """Round-robin endpoint selection"""
        counter = self.routing_counters.get(route_id, 0)
        selected = endpoints[counter % len(endpoints)]
        self.routing_counters[route_id] = counter + 1
        return selected
    
    def _quantum_coherence_selection(self, endpoints: List[ServiceEndpoint]) -> ServiceEndpoint:
        """Select endpoint with highest quantum coherence"""
        return max(endpoints, key=lambda e: e.quantum_coherence)
    
    def _consciousness_level_selection(self, endpoints: List[ServiceEndpoint]) -> ServiceEndpoint:
        """Select endpoint with highest consciousness level"""
        return max(endpoints, key=lambda e: e.consciousness_level)
    
    def _genetic_fitness_selection(self, endpoints: List[ServiceEndpoint]) -> ServiceEndpoint:
        """Select endpoint with highest genetic fitness"""
        return max(endpoints, key=lambda e: e.genetic_fitness)
    
    def _least_connections_selection(self, endpoints: List[ServiceEndpoint]) -> ServiceEndpoint:
        """Select endpoint with least active connections"""
        return min(endpoints, key=lambda e: e.current_connections)
    
    def _weighted_random_selection(self, endpoints: List[ServiceEndpoint]) -> ServiceEndpoint:
        """Weighted random selection based on endpoint weights"""
        import random
        
        # Calculate weights incorporating quantum metrics
        weights = []
        for endpoint in endpoints:
            quantum_score = (
                endpoint.quantum_coherence * 0.4 +
                (endpoint.consciousness_level / 6.0) * 0.3 +
                endpoint.genetic_fitness * 0.3
            )
            weight = endpoint.weight * quantum_score * (1.0 - endpoint.error_rate)
            weights.append(weight)
        
        # Weighted random selection
        total_weight = sum(weights)
        if total_weight == 0:
            return random.choice(endpoints)
        
        r = random.uniform(0, total_weight)
        cumulative = 0
        for i, weight in enumerate(weights):
            cumulative += weight
            if r <= cumulative:
                return endpoints[i]
        
        return endpoints[-1]  # Fallback

class RateLimiter:
    """Redis-based rate limiter with quantum awareness"""
    
    def __init__(self, redis_client: Optional[Any] = None):
        self.redis = redis_client
        self.local_cache: Dict[str, List[float]] = {}
        
    async def is_rate_limited(self, 
                            key: str, 
                            limit: int, 
                            window: int = 60,
                            quantum_boost: bool = False) -> bool:
        """Check if request should be rate limited"""
        
        current_time = time.time()
        
        # Apply quantum boost (higher limits for quantum-enhanced users)
        if quantum_boost:
            limit = int(limit * 1.5)
        
        if self.redis:
            # Redis-based distributed rate limiting
            return await self._redis_rate_limit(key, limit, window, current_time)
        else:
            # Local in-memory rate limiting
            return self._local_rate_limit(key, limit, window, current_time)
    
    async def _redis_rate_limit(self, key: str, limit: int, window: int, current_time: float) -> bool:
        """Redis sliding window rate limiter"""
        try:
            pipe = self.redis.pipeline()
            pipe.zremrangebyscore(key, 0, current_time - window)
            pipe.zcard(key)
            pipe.zadd(key, {str(current_time): current_time})
            pipe.expire(key, window)
            results = await pipe.execute()
            
            current_requests = results[1]
            return current_requests >= limit
        except:
            return False  # Allow requests if Redis is unavailable
    
    def _local_rate_limit(self, key: str, limit: int, window: int, current_time: float) -> bool:
        """Local memory sliding window rate limiter"""
        if key not in self.local_cache:
            self.local_cache[key] = []
        
        # Clean old entries
        cutoff_time = current_time - window
        self.local_cache[key] = [
            timestamp for timestamp in self.local_cache[key]
            if timestamp > cutoff_time
        ]
        
        # Check limit
        if len(self.local_cache[key]) >= limit:
            return True
        
        # Add current request
        self.local_cache[key].append(current_time)
        return False

class QuantumApiGateway:
    """
    Enterprise Quantum API Gateway with consciousness-aware routing and 
    quantum-enhanced load balancing for microservices integration.
    """
    
    def __init__(self,
                 hive_id: str,
                 security_manager: QuantumSecurityManager,
                 quantum_logger: QuantumLogger,
                 redis_url: Optional[str] = None,
                 enable_caching: bool = True):
        
        self.hive_id = hive_id
        self.security_manager = security_manager
        self.logger = quantum_logger
        self.enable_caching = enable_caching
        
        # Core components
        self.load_balancer = QuantumLoadBalancer()
        self.rate_limiter = RateLimiter()
        self.routes: Dict[str, RouteConfig] = {}
        self.middleware_stack: List[Callable] = []
        
        # Caching and performance
        self.response_cache: Dict[str, Dict[str, Any]] = {}
        self.request_metrics: List[RequestMetrics] = []
        
        # HTTP client for backend requests
        self.http_client: Optional[httpx.AsyncClient] = None
        
        # Initialize FastAPI if available
        if FASTAPI_AVAILABLE:
            self.app = FastAPI(
                title="Quantum Hive API Gateway",
                description="Enterprise quantum-enhanced microservices gateway",
                version="1.0.0"
            )
            self._setup_fastapi()
        
        # Initialize Redis connection
        self.redis = None
        if redis_url:
            asyncio.create_task(self._init_redis(redis_url))
        
        self.logger.info("QuantumApiGateway initialized", hive_id=hive_id)
    
    async def _init_redis(self, redis_url: str):
        """Initialize Redis connection for caching and rate limiting"""
        try:
            if 'aioredis' in globals():
                self.redis = await aioredis.from_url(redis_url)
                self.rate_limiter.redis = self.redis
                self.logger.info("Redis connection established")
        except Exception as e:
            self.logger.error("Failed to connect to Redis", exception=e)
    
    def _setup_fastapi(self):
        """Configure FastAPI application with quantum middleware"""
        
        # CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Compression middleware  
        self.app.add_middleware(GZipMiddleware, minimum_size=1000)
        
        # Custom quantum middleware
        @self.app.middleware("http")
        async def quantum_middleware(request: Request, call_next):
            return await self._process_request_middleware(request, call_next)
        
        # Health check endpoint
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "hive_id": self.hive_id}
        
        # Metrics endpoint
        @self.app.get("/metrics")
        async def gateway_metrics():
            return self._get_gateway_metrics()
        
        # Dynamic route handler
        @self.app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
        async def handle_request(request: Request, path: str):
            return await self._handle_api_request(request, path)
    
    def register_service(self, endpoint: ServiceEndpoint):
        """Register a backend microservice endpoint"""
        self.load_balancer.register_endpoint(endpoint)
        self.logger.info(f"Service registered: {endpoint.name}",
                        endpoint_id=endpoint.endpoint_id,
                        host=endpoint.host,
                        port=endpoint.port)
    
    def register_route(self, route: RouteConfig):
        """Register an API route configuration"""
        self.routes[route.route_id] = route
        self.logger.info(f"Route registered: {route.path_pattern}",
                        route_id=route.route_id,
                        methods=[m.value for m in route.methods])
    
    def add_middleware(self, middleware_func: Callable):
        """Add custom middleware to the processing stack"""
        self.middleware_stack.append(middleware_func)
        self.logger.info("Custom middleware added")
    
    async def _process_request_middleware(self, request: Request, call_next):
        """Process request through quantum middleware stack"""
        start_time = time.time()
        request_id = hashlib.md5(f"{start_time}{request.url}".encode()).hexdigest()[:12]
        
        # Add quantum context to request
        request.state.quantum_context = {
            "request_id": request_id,
            "start_time": start_time,
            "hive_id": self.hive_id
        }
        
        # Log request start
        self.logger.info("API request received",
                        request_id=request_id,
                        method=request.method,
                        path=str(request.url),
                        user_agent=request.headers.get("user-agent", "unknown"))
        
        try:
            # Process through custom middleware
            for middleware in self.middleware_stack:
                request = await middleware(request)
            
            # Process request
            response = await call_next(request)
            
            # Add quantum headers
            response.headers["X-Quantum-Hive-ID"] = self.hive_id
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Quantum-Coherence"] = "0.95"  # Example value
            
            # Log response
            duration = time.time() - start_time
            self.logger.info("API request completed",
                           request_id=request_id,
                           status_code=response.status_code,
                           duration=duration,
                           event_category="api_response")
            
            return response
            
        except Exception as e:
            self.logger.error("API request failed",
                            request_id=request_id,
                            exception=e)
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "request_id": request_id}
            )
    
    async def _handle_api_request(self, request: Request, path: str) -> Response:
        """Handle API request with quantum routing"""
        
        # Find matching route
        route_config = self._match_route(request.method, f"/{path}")
        if not route_config:
            raise HTTPException(status_code=404, detail="Route not found")
        
        # Authentication check
        if route_config.require_auth:
            security_context = await self._authenticate_request(request)
            if not security_context:
                raise HTTPException(status_code=401, detail="Authentication required")
            
            # Quantum clearance check
            if security_context.quantum_clearance < route_config.require_quantum_clearance:
                raise HTTPException(status_code=403, detail="Insufficient quantum clearance")
        
        # Rate limiting
        if route_config.rate_limit:
            user_key = self._get_rate_limit_key(request)
            is_limited = await self.rate_limiter.is_rate_limited(
                user_key, 
                route_config.rate_limit,
                quantum_boost=route_config.quantum_enhancement
            )
            if is_limited:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        # Check cache
        if route_config.cache_ttl and request.method == "GET":
            cached_response = await self._get_cached_response(request, route_config)
            if cached_response:
                return JSONResponse(cached_response["content"])
        
        # Select backend endpoint
        endpoint = self.load_balancer.select_endpoint(route_config, {
            "request": request,
            "quantum_context": getattr(request.state, 'quantum_context', {})
        })
        
        if not endpoint:
            raise HTTPException(status_code=503, detail="No healthy backend services available")
        
        # Proxy request to backend
        try:
            response = await self._proxy_request(request, endpoint, path)
            
            # Cache response if configured
            if route_config.cache_ttl and request.method == "GET" and response.status_code == 200:
                await self._cache_response(request, route_config, response)
            
            return response
            
        except Exception as e:
            self.logger.error("Backend request failed", 
                            endpoint_id=endpoint.endpoint_id,
                            exception=e)
            raise HTTPException(status_code=502, detail="Backend service error")
    
    def _match_route(self, method: str, path: str) -> Optional[RouteConfig]:
        """Find matching route configuration"""
        for route_config in self.routes.values():
            # Check if method matches
            if not any(m.value == method for m in route_config.methods):
                continue
                
            # Check if path matches pattern
            pattern = route_config.path_pattern.replace("*", ".*")
            if re.match(f"^{pattern}$", path):
                return route_config
        
        return None
    
    async def _authenticate_request(self, request: Request) -> Optional[SecurityContext]:
        """Authenticate API request using quantum security manager"""
        
        # Get authorization header
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None
        
        token = auth_header[7:]  # Remove "Bearer " prefix
        
        # Verify JWT token
        security_context = self.security_manager.verify_jwt_token(token)
        
        if security_context:
            # Log authentication success
            self.logger.info("Request authenticated",
                           user_id=security_context.user_id,
                           quantum_clearance=security_context.quantum_clearance)
        
        return security_context
    
    def _get_rate_limit_key(self, request: Request) -> str:
        """Generate rate limiting key from request"""
        # Use IP address and user ID if available
        client_ip = request.client.host if request.client else "unknown"
        auth_header = request.headers.get("Authorization", "")
        
        if auth_header:
            # Include user context in rate limit key
            user_hash = hashlib.md5(auth_header.encode()).hexdigest()[:8]
            return f"rate_limit:{client_ip}:{user_hash}"
        else:
            return f"rate_limit:{client_ip}"
    
    async def _get_cached_response(self, request: Request, route_config: RouteConfig) -> Optional[Dict[str, Any]]:
        """Get cached response if available and not expired"""
        cache_key = self._generate_cache_key(request)
        
        if self.redis:
            try:
                cached_data = await self.redis.get(cache_key)
                if cached_data:
                    return json.loads(cached_data)
            except:
                pass
        else:
            # Local cache
            cached_entry = self.response_cache.get(cache_key)
            if cached_entry:
                if time.time() - cached_entry["timestamp"] < route_config.cache_ttl:
                    return cached_entry
                else:
                    del self.response_cache[cache_key]
        
        return None
    
    async def _cache_response(self, request: Request, route_config: RouteConfig, response: Response):
        """Cache response for future requests"""
        cache_key = self._generate_cache_key(request)
        
        # Don't cache large responses or errors
        if hasattr(response, 'body') and len(response.body) > 100000:
            return
        
        cached_data = {
            "content": response.body.decode() if hasattr(response, 'body') else "",
            "timestamp": time.time()
        }
        
        if self.redis:
            try:
                await self.redis.setex(
                    cache_key, 
                    route_config.cache_ttl, 
                    json.dumps(cached_data)
                )
            except:
                pass
        else:
            # Local cache with size limit
            if len(self.response_cache) > 1000:
                # Remove oldest entries
                oldest_keys = sorted(
                    self.response_cache.keys(),
                    key=lambda k: self.response_cache[k]["timestamp"]
                )[:100]
                for key in oldest_keys:
                    del self.response_cache[key]
            
            self.response_cache[cache_key] = cached_data
    
    def _generate_cache_key(self, request: Request) -> str:
        """Generate cache key from request"""
        key_parts = [
            request.method,
            str(request.url.path),
            str(request.url.query)
        ]
        
        # Include relevant headers
        for header in ["accept", "accept-language"]:
            if header in request.headers:
                key_parts.append(f"{header}:{request.headers[header]}")
        
        key_string = "|".join(key_parts)
        return f"cache:{hashlib.md5(key_string.encode()).hexdigest()}"
    
    async def _proxy_request(self, request: Request, endpoint: ServiceEndpoint, path: str) -> Response:
        """Proxy request to backend service"""
        
        if not self.http_client:
            self.http_client = httpx.AsyncClient(timeout=30.0)
        
        # Build backend URL
        backend_url = f"http://{endpoint.host}:{endpoint.port}{endpoint.path_prefix}/{path}"
        
        # Prepare headers
        headers = dict(request.headers)
        headers["X-Forwarded-For"] = request.client.host if request.client else "unknown"
        headers["X-Quantum-Hive-ID"] = self.hive_id
        headers["X-Quantum-Coherence"] = str(endpoint.quantum_coherence)
        headers["X-Consciousness-Level"] = str(endpoint.consciousness_level)
        
        # Get request body if present
        body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()
        
        # Track connection
        endpoint.current_connections += 1
        start_time = time.time()
        
        try:
            # Make backend request
            backend_response = await self.http_client.request(
                method=request.method,
                url=backend_url,
                headers=headers,
                params=dict(request.query_params),
                content=body
            )
            
            # Update endpoint metrics
            response_time = time.time() - start_time
            endpoint.response_time_avg = (
                endpoint.response_time_avg * 0.9 + response_time * 0.1
            )
            
            if backend_response.status_code >= 500:
                endpoint.error_rate = min(endpoint.error_rate + 0.01, 1.0)
            else:
                endpoint.error_rate = max(endpoint.error_rate - 0.001, 0.0)
            
            # Create response
            response = Response(
                content=backend_response.content,
                status_code=backend_response.status_code,
                headers=dict(backend_response.headers)
            )
            
            # Record successful request metrics
            self._record_request_metrics(request, endpoint, response_time, backend_response.status_code)
            
            return response
            
        finally:
            endpoint.current_connections -= 1
    
    def _record_request_metrics(self, request: Request, endpoint: ServiceEndpoint, 
                              response_time: float, status_code: int):
        """Record request metrics for monitoring"""
        metrics = RequestMetrics(
            request_id=getattr(request.state, 'quantum_context', {}).get('request_id', 'unknown'),
            route_id="unknown",  # Would be set by route matching
            endpoint_id=endpoint.endpoint_id,
            method=request.method,
            path=str(request.url.path),
            start_time=datetime.now(timezone.utc),
            status_code=status_code,
            response_time=response_time,
            quantum_context={
                "coherence": endpoint.quantum_coherence,
                "consciousness": endpoint.consciousness_level,
                "fitness": endpoint.genetic_fitness
            }
        )
        
        self.request_metrics.append(metrics)
        
        # Keep only recent metrics (last 10000 requests)
        if len(self.request_metrics) > 10000:
            self.request_metrics = self.request_metrics[-5000:]
    
    def _get_gateway_metrics(self) -> Dict[str, Any]:
        """Get comprehensive gateway metrics"""
        
        # Calculate request statistics
        recent_requests = [
            m for m in self.request_metrics
            if m.start_time > datetime.now(timezone.utc).replace(hour=0, minute=0, second=0)
        ]
        
        total_requests_today = len(recent_requests)
        avg_response_time = sum(m.response_time for m in recent_requests if m.response_time) / max(len(recent_requests), 1)
        error_rate = len([m for m in recent_requests if m.status_code >= 400]) / max(total_requests_today, 1)
        
        # Endpoint health
        healthy_endpoints = len([e for e in self.load_balancer.endpoints.values() if e.is_healthy])
        total_endpoints = len(self.load_balancer.endpoints)
        
        return {
            "hive_id": self.hive_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "gateway_status": "healthy",
            "requests_today": total_requests_today,
            "average_response_time": avg_response_time,
            "error_rate": error_rate,
            "registered_routes": len(self.routes),
            "healthy_endpoints": f"{healthy_endpoints}/{total_endpoints}",
            "cache_enabled": self.enable_caching,
            "redis_connected": self.redis is not None,
            "quantum_features": {
                "consciousness_routing": True,
                "coherence_balancing": True,
                "genetic_fitness_weighting": True,
                "quantum_clearance_auth": True
            }
        }
    
    async def start_server(self, host: str = "0.0.0.0", port: int = 8080):
        """Start the API Gateway server"""
        if not FASTAPI_AVAILABLE:
            raise RuntimeError("FastAPI not available - install with: pip install fastapi uvicorn")
        
        config = uvicorn.Config(
            app=self.app,
            host=host,
            port=port,
            log_level="info",
            access_log=True
        )
        
        server = uvicorn.Server(config)
        
        self.logger.info(f"Starting Quantum API Gateway on {host}:{port}")
        await server.serve()

# Example usage and testing
if __name__ == "__main__":
    async def test_api_gateway():
        from deployment.security.quantum_security_framework import QuantumSecurityManager
        from deployment.logging.structured_logger import create_quantum_logger
        
        print("🌐 Testing Quantum API Gateway...")
        
        # Initialize components
        security_manager = QuantumSecurityManager(
            hive_id="test_gateway_hive"
        )
        
        quantum_logger = create_quantum_logger(
            hive_id="test_gateway_hive",
            component="api_gateway"
        )
        
        # Initialize API Gateway
        gateway = QuantumApiGateway(
            hive_id="test_gateway_hive",
            security_manager=security_manager,
            quantum_logger=quantum_logger,
            enable_caching=True
        )
        
        # Register sample backend services
        gateway.register_service(ServiceEndpoint(
            endpoint_id="quantum_core_1",
            name="Quantum Core Service",
            host="localhost",
            port=8081,
            path_prefix="/api/v1",
            quantum_coherence=0.95,
            consciousness_level=4,
            genetic_fitness=0.87
        ))
        
        gateway.register_service(ServiceEndpoint(
            endpoint_id="genetic_worker_1", 
            name="Genetic Programming Worker",
            host="localhost",
            port=8082,
            path_prefix="/genetic/v1",
            quantum_coherence=0.88,
            consciousness_level=2,
            genetic_fitness=0.92
        ))
        
        # Register sample routes
        gateway.register_route(RouteConfig(
            route_id="quantum_api",
            path_pattern="/api/quantum/*",
            methods=[ApiMethod.GET, ApiMethod.POST],
            target_services=["quantum_core_1"],
            routing_strategy=RoutingStrategy.QUANTUM_COHERENCE,
            require_quantum_clearance=2,
            rate_limit=100,
            cache_ttl=60
        ))
        
        gateway.register_route(RouteConfig(
            route_id="genetic_api",
            path_pattern="/api/genetic/*", 
            methods=[ApiMethod.GET, ApiMethod.POST, ApiMethod.PUT],
            target_services=["genetic_worker_1"],
            routing_strategy=RoutingStrategy.GENETIC_FITNESS,
            require_quantum_clearance=1,
            rate_limit=200
        ))
        
        # Show configuration
        print("✅ API Gateway configured:")
        print(f"   Services: {len(gateway.load_balancer.endpoints)}")
        print(f"   Routes: {len(gateway.routes)}")
        
        # Get metrics
        metrics = gateway._get_gateway_metrics()
        print(f"\n📊 Gateway Metrics:")
        print(f"   Status: {metrics['gateway_status']}")
        print(f"   Routes: {metrics['registered_routes']}")
        print(f"   Endpoints: {metrics['healthy_endpoints']}")
        print(f"   Cache: {metrics['cache_enabled']}")
        
        print("\n🚀 API Gateway test completed!")
        print("   To start server: await gateway.start_server()")
    
    # Run the test
    asyncio.run(test_api_gateway())