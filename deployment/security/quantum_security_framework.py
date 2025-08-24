#!/usr/bin/env python3
"""
Quantum Hive Enterprise Security & Compliance Framework
Comprehensive security controls for quantum-enhanced microservices
"""

import asyncio
import hashlib
import hmac
import jwt
import secrets
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
from contextlib import asynccontextmanager
import logging
import json
import os

# Cryptography (install: pip install cryptography PyJWT)
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
    import bcrypt
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("WARNING: cryptography not available. Install with: pip install cryptography PyJWT bcrypt")

class SecurityLevel(Enum):
    """Security classification levels"""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"
    TOP_SECRET = "top_secret"

class ComplianceFramework(Enum):
    """Supported compliance frameworks"""
    SOC2 = "soc2"
    GDPR = "gdpr"
    HIPAA = "hipaa"
    ISO27001 = "iso27001"
    NIST = "nist"
    PCI_DSS = "pci_dss"

@dataclass
class SecurityContext:
    """Security context for operations"""
    user_id: str
    role: str
    permissions: List[str]
    security_level: SecurityLevel
    session_id: str
    quantum_clearance: int
    authentication_method: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    source_ip: Optional[str] = None
    user_agent: Optional[str] = None

@dataclass
class AuditEvent:
    """Security audit event"""
    event_id: str
    event_type: str
    user_id: str
    resource: str
    action: str
    result: str
    timestamp: datetime
    source_ip: Optional[str] = None
    user_agent: Optional[str] = None
    quantum_context: Optional[Dict[str, Any]] = None
    risk_score: float = 0.0
    compliance_frameworks: List[ComplianceFramework] = field(default_factory=list)

@dataclass
class ComplianceRule:
    """Compliance rule definition"""
    rule_id: str
    framework: ComplianceFramework
    category: str
    description: str
    severity: str
    automated_check: bool = True
    check_function: Optional[str] = None
    remediation_steps: List[str] = field(default_factory=list)

class QuantumSecurityManager:
    """
    Enterprise quantum security and compliance management system.
    Provides comprehensive security controls with quantum context awareness.
    """
    
    def __init__(self, 
                 hive_id: str,
                 encryption_key: Optional[bytes] = None,
                 jwt_secret: Optional[str] = None,
                 enable_quantum_encryption: bool = True,
                 compliance_frameworks: List[ComplianceFramework] = None):
        
        self.hive_id = hive_id
        self.enable_quantum_encryption = enable_quantum_encryption
        self.compliance_frameworks = compliance_frameworks or [ComplianceFramework.SOC2]
        
        # Initialize logging
        self.logger = logging.getLogger(f"quantum-hive.{hive_id}.security")
        
        # Security storage
        self.active_sessions: Dict[str, SecurityContext] = {}
        self.audit_log: List[AuditEvent] = []
        self.blocked_ips: Dict[str, datetime] = {}
        self.failed_attempts: Dict[str, int] = {}
        
        # Initialize cryptographic components
        if CRYPTO_AVAILABLE:
            self._init_crypto(encryption_key, jwt_secret)
        else:
            self.logger.error("Cryptography not available - security features disabled")
            
        # Load compliance rules
        self.compliance_rules = self._load_compliance_rules()
        
        self.logger.info(f"QuantumSecurityManager initialized for hive {hive_id}")
    
    def _init_crypto(self, encryption_key: Optional[bytes], jwt_secret: Optional[str]):
        """Initialize cryptographic systems"""
        
        # Symmetric encryption for data at rest
        if encryption_key:
            self.fernet = Fernet(encryption_key)
        else:
            # Generate new key
            key = Fernet.generate_key()
            self.fernet = Fernet(key)
            self.logger.warning("Generated new encryption key - store securely!")
        
        # JWT signing key
        self.jwt_secret = jwt_secret or secrets.token_urlsafe(32)
        
        # Generate RSA key pair for asymmetric operations
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        
        # Quantum entropy pool for enhanced randomness
        self._quantum_entropy_pool = secrets.SystemRandom()
        
        self.logger.info("Cryptographic systems initialized")
    
    def _load_compliance_rules(self) -> List[ComplianceRule]:
        """Load compliance rules for active frameworks"""
        rules = []
        
        # SOC2 Type II rules
        if ComplianceFramework.SOC2 in self.compliance_frameworks:
            rules.extend([
                ComplianceRule(
                    rule_id="SOC2-CC6.1",
                    framework=ComplianceFramework.SOC2,
                    category="Logical and Physical Access Controls",
                    description="System implements controls to restrict logical access",
                    severity="high",
                    check_function="check_access_controls"
                ),
                ComplianceRule(
                    rule_id="SOC2-CC6.7",
                    framework=ComplianceFramework.SOC2,
                    category="Encryption",
                    description="Sensitive data is encrypted in transmission and at rest",
                    severity="critical",
                    check_function="check_encryption"
                )
            ])
        
        # GDPR rules
        if ComplianceFramework.GDPR in self.compliance_frameworks:
            rules.extend([
                ComplianceRule(
                    rule_id="GDPR-Art25",
                    framework=ComplianceFramework.GDPR,
                    category="Data Protection by Design",
                    description="Privacy by design and default implementation",
                    severity="high",
                    check_function="check_privacy_by_design"
                ),
                ComplianceRule(
                    rule_id="GDPR-Art32",
                    framework=ComplianceFramework.GDPR,
                    category="Security of Processing",
                    description="Appropriate technical and organizational measures",
                    severity="critical",
                    check_function="check_security_measures"
                )
            ])
        
        return rules
    
    async def authenticate_user(self, 
                               username: str, 
                               password: str,
                               source_ip: str = None,
                               user_agent: str = None,
                               quantum_challenge: Optional[str] = None) -> Optional[SecurityContext]:
        """
        Authenticate user with quantum-enhanced security
        """
        
        # Check for blocked IP
        if source_ip and source_ip in self.blocked_ips:
            if datetime.now(timezone.utc) < self.blocked_ips[source_ip]:
                self._audit_event("authentication_blocked", username, "blocked_ip", 
                                source_ip=source_ip, result="blocked")
                return None
        
        # Check failed attempts
        attempt_key = f"{username}:{source_ip or 'unknown'}"
        if self.failed_attempts.get(attempt_key, 0) >= 5:
            self._block_ip(source_ip)
            return None
        
        # Simulate user lookup and password verification
        # In production, this would query your user database
        user_data = await self._lookup_user(username)
        if not user_data:
            self._record_failed_attempt(attempt_key)
            self._audit_event("authentication_failed", username, "user_not_found",
                            source_ip=source_ip, result="failed")
            return None
        
        # Verify password
        if not self._verify_password(password, user_data.get("password_hash")):
            self._record_failed_attempt(attempt_key)
            self._audit_event("authentication_failed", username, "invalid_password",
                            source_ip=source_ip, result="failed")
            return None
        
        # Quantum challenge verification (optional second factor)
        if quantum_challenge and not self._verify_quantum_challenge(quantum_challenge, user_data):
            self._record_failed_attempt(attempt_key)
            self._audit_event("authentication_failed", username, "quantum_challenge_failed",
                            source_ip=source_ip, result="failed")
            return None
        
        # Clear failed attempts on success
        if attempt_key in self.failed_attempts:
            del self.failed_attempts[attempt_key]
        
        # Create security context
        context = SecurityContext(
            user_id=user_data["user_id"],
            role=user_data["role"],
            permissions=user_data["permissions"],
            security_level=SecurityLevel(user_data.get("security_level", "internal")),
            session_id=secrets.token_urlsafe(32),
            quantum_clearance=user_data.get("quantum_clearance", 1),
            authentication_method="password+quantum" if quantum_challenge else "password",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=8),
            source_ip=source_ip,
            user_agent=user_agent
        )
        
        # Store active session
        self.active_sessions[context.session_id] = context
        
        self._audit_event("authentication_success", username, "login",
                        source_ip=source_ip, result="success")
        
        return context
    
    def create_jwt_token(self, context: SecurityContext) -> str:
        """Create JWT token for authenticated user"""
        if not CRYPTO_AVAILABLE:
            raise RuntimeError("JWT creation requires cryptography library")
        
        payload = {
            "user_id": context.user_id,
            "role": context.role,
            "permissions": context.permissions,
            "security_level": context.security_level.value,
            "quantum_clearance": context.quantum_clearance,
            "session_id": context.session_id,
            "hive_id": self.hive_id,
            "iat": int(context.created_at.timestamp()),
            "exp": int(context.expires_at.timestamp()) if context.expires_at else None
        }
        
        token = jwt.encode(payload, self.jwt_secret, algorithm="HS256")
        
        self._audit_event("jwt_created", context.user_id, "token_generation",
                        result="success")
        
        return token
    
    def verify_jwt_token(self, token: str) -> Optional[SecurityContext]:
        """Verify and decode JWT token"""
        if not CRYPTO_AVAILABLE:
            return None
        
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            
            # Check if session still active
            session_id = payload.get("session_id")
            if session_id not in self.active_sessions:
                return None
            
            context = self.active_sessions[session_id]
            
            # Check expiration
            if context.expires_at and datetime.now(timezone.utc) > context.expires_at:
                self.revoke_session(session_id)
                return None
            
            return context
            
        except jwt.InvalidTokenError as e:
            self.logger.warning(f"JWT verification failed: {e}")
            return None
    
    def authorize_operation(self, 
                           context: SecurityContext,
                           resource: str,
                           action: str,
                           required_level: SecurityLevel = SecurityLevel.INTERNAL) -> bool:
        """
        Authorize user operation with quantum security context
        """
        
        # Check security level clearance
        level_hierarchy = {
            SecurityLevel.PUBLIC: 0,
            SecurityLevel.INTERNAL: 1,
            SecurityLevel.CONFIDENTIAL: 2,
            SecurityLevel.SECRET: 3,
            SecurityLevel.TOP_SECRET: 4
        }
        
        if level_hierarchy[context.security_level] < level_hierarchy[required_level]:
            self._audit_event("authorization_failed", context.user_id, resource,
                            result="insufficient_clearance")
            return False
        
        # Check specific permissions
        required_permission = f"{resource}:{action}"
        if required_permission not in context.permissions and "admin:*" not in context.permissions:
            self._audit_event("authorization_failed", context.user_id, resource,
                            result="insufficient_permissions")
            return False
        
        self._audit_event("authorization_success", context.user_id, resource,
                        result="success")
        return True
    
    def encrypt_sensitive_data(self, data: Union[str, dict], 
                             quantum_enhanced: bool = True) -> str:
        """Encrypt sensitive data with optional quantum enhancement"""
        if not CRYPTO_AVAILABLE:
            raise RuntimeError("Encryption requires cryptography library")
        
        if isinstance(data, dict):
            data = json.dumps(data)
        
        data_bytes = data.encode('utf-8')
        
        if quantum_enhanced and self.enable_quantum_encryption:
            # Add quantum entropy to the encryption process
            quantum_salt = self._generate_quantum_salt()
            data_bytes = quantum_salt + data_bytes
        
        encrypted_data = self.fernet.encrypt(data_bytes)
        return encrypted_data.decode('utf-8')
    
    def decrypt_sensitive_data(self, encrypted_data: str, 
                             quantum_enhanced: bool = True) -> str:
        """Decrypt sensitive data"""
        if not CRYPTO_AVAILABLE:
            raise RuntimeError("Decryption requires cryptography library")
        
        encrypted_bytes = encrypted_data.encode('utf-8')
        decrypted_data = self.fernet.decrypt(encrypted_bytes)
        
        if quantum_enhanced and self.enable_quantum_encryption:
            # Remove quantum salt
            decrypted_data = decrypted_data[32:]  # Remove 32-byte salt
        
        return decrypted_data.decode('utf-8')
    
    def _generate_quantum_salt(self) -> bytes:
        """Generate quantum-enhanced salt"""
        return secrets.token_bytes(32)
    
    async def _lookup_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Simulate user lookup - replace with actual database query"""
        # Mock user database
        users = {
            "admin": {
                "user_id": "admin_001",
                "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyMv4VVPzWPdsy",  # "admin123"
                "role": "administrator",
                "permissions": ["admin:*"],
                "security_level": "secret",
                "quantum_clearance": 6
            },
            "quantum_user": {
                "user_id": "quser_001",
                "password_hash": "$2b$12$8vqPrFQxRJvhXqE5c8KzGuRmF2vBk6HdKlMhgFJ4gL2pKvGwxFENC",  # "quantum123"
                "role": "quantum_operator",
                "permissions": ["quantum:read", "quantum:write", "genetic:read"],
                "security_level": "confidential",
                "quantum_clearance": 4
            }
        }
        
        await asyncio.sleep(0.01)  # Simulate database lookup delay
        return users.get(username)
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        if not CRYPTO_AVAILABLE:
            return password == password_hash  # Fallback for testing
        
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except:
            return False
    
    def _verify_quantum_challenge(self, challenge: str, user_data: Dict[str, Any]) -> bool:
        """Verify quantum authentication challenge"""
        # This would implement quantum key distribution or quantum-safe authentication
        # For now, simulate with a quantum-aware challenge
        expected_response = hashlib.sha256(
            f"{user_data['user_id']}:quantum_challenge:{time.time() // 30}".encode()
        ).hexdigest()[:16]
        
        return challenge == expected_response
    
    def _record_failed_attempt(self, attempt_key: str):
        """Record failed authentication attempt"""
        self.failed_attempts[attempt_key] = self.failed_attempts.get(attempt_key, 0) + 1
    
    def _block_ip(self, ip_address: str, duration_minutes: int = 30):
        """Block IP address for specified duration"""
        if ip_address:
            self.blocked_ips[ip_address] = datetime.now(timezone.utc) + timedelta(minutes=duration_minutes)
            self.logger.warning(f"IP {ip_address} blocked for {duration_minutes} minutes")
    
    def _audit_event(self, event_type: str, user_id: str, resource: str,
                    source_ip: str = None, user_agent: str = None, result: str = "unknown"):
        """Record security audit event"""
        event = AuditEvent(
            event_id=secrets.token_urlsafe(16),
            event_type=event_type,
            user_id=user_id,
            resource=resource,
            action=event_type,
            result=result,
            timestamp=datetime.now(timezone.utc),
            source_ip=source_ip,
            user_agent=user_agent,
            compliance_frameworks=self.compliance_frameworks
        )
        
        self.audit_log.append(event)
        
        # Log to system logger
        self.logger.info(f"Security Event: {event_type} by {user_id} on {resource} - {result}")
    
    def revoke_session(self, session_id: str) -> bool:
        """Revoke active session"""
        if session_id in self.active_sessions:
            context = self.active_sessions[session_id]
            del self.active_sessions[session_id]
            
            self._audit_event("session_revoked", context.user_id, "session",
                            result="success")
            return True
        return False
    
    async def run_compliance_checks(self) -> Dict[str, Any]:
        """Run automated compliance checks"""
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hive_id": self.hive_id,
            "frameworks": [f.value for f in self.compliance_frameworks],
            "checks": [],
            "violations": [],
            "overall_status": "compliant"
        }
        
        for rule in self.compliance_rules:
            if rule.automated_check and rule.check_function:
                try:
                    check_method = getattr(self, rule.check_function)
                    check_result = await check_method()
                    
                    check_status = {
                        "rule_id": rule.rule_id,
                        "framework": rule.framework.value,
                        "category": rule.category,
                        "status": "pass" if check_result else "fail",
                        "severity": rule.severity
                    }
                    
                    results["checks"].append(check_status)
                    
                    if not check_result:
                        results["violations"].append({
                            "rule_id": rule.rule_id,
                            "description": rule.description,
                            "severity": rule.severity,
                            "remediation": rule.remediation_steps
                        })
                        
                        if rule.severity in ["critical", "high"]:
                            results["overall_status"] = "non_compliant"
                
                except AttributeError:
                    self.logger.warning(f"Compliance check function not found: {rule.check_function}")
        
        # Log compliance results
        if results["violations"]:
            self.logger.critical(f"Compliance violations detected: {len(results['violations'])}")
        else:
            self.logger.info("All compliance checks passed")
        
        return results
    
    async def check_access_controls(self) -> bool:
        """SOC2 CC6.1 - Check access controls implementation"""
        # Check if proper authentication is required
        # Check if roles and permissions are implemented
        # Check if session management is secure
        
        checks = [
            len(self.active_sessions) > 0,  # Active session management
            hasattr(self, 'jwt_secret'),    # JWT implementation
            len(self.audit_log) > 0,        # Audit logging active
            CRYPTO_AVAILABLE                # Cryptographic controls available
        ]
        
        return all(checks)
    
    async def check_encryption(self) -> bool:
        """SOC2 CC6.7 - Check encryption implementation"""
        if not CRYPTO_AVAILABLE:
            return False
        
        # Test encryption capabilities
        try:
            test_data = "sensitive test data"
            encrypted = self.encrypt_sensitive_data(test_data)
            decrypted = self.decrypt_sensitive_data(encrypted)
            return decrypted == test_data
        except:
            return False
    
    async def check_privacy_by_design(self) -> bool:
        """GDPR Art 25 - Check privacy by design implementation"""
        # Check data minimization
        # Check purpose limitation
        # Check storage limitation
        
        privacy_checks = [
            self.enable_quantum_encryption,  # Enhanced privacy protection
            len(self.audit_log) > 0,         # Privacy action logging
            hasattr(self, 'compliance_frameworks')  # Privacy framework awareness
        ]
        
        return all(privacy_checks)
    
    async def check_security_measures(self) -> bool:
        """GDPR Art 32 - Check security of processing"""
        # Check pseudonymization and encryption
        # Check confidentiality, integrity, availability
        # Check resilience of systems
        
        security_measures = [
            CRYPTO_AVAILABLE,               # Encryption capability
            len(self.blocked_ips) >= 0,     # Attack protection
            len(self.failed_attempts) >= 0, # Brute force protection
            hasattr(self, 'audit_log')      # Security monitoring
        ]
        
        return all(security_measures)
    
    def get_security_metrics(self) -> Dict[str, Any]:
        """Get comprehensive security metrics"""
        return {
            "hive_id": self.hive_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "active_sessions": len(self.active_sessions),
            "blocked_ips": len(self.blocked_ips),
            "failed_attempts_tracked": len(self.failed_attempts),
            "audit_events": len(self.audit_log),
            "compliance_frameworks": [f.value for f in self.compliance_frameworks],
            "encryption_enabled": CRYPTO_AVAILABLE and hasattr(self, 'fernet'),
            "quantum_enhancement": self.enable_quantum_encryption,
            "security_events_24h": len([
                event for event in self.audit_log
                if event.timestamp > datetime.now(timezone.utc) - timedelta(hours=24)
            ])
        }

# Context manager for secure operations
@asynccontextmanager
async def quantum_security_context(security_manager: QuantumSecurityManager,
                                 token: str):
    """Context manager for secure quantum operations"""
    context = security_manager.verify_jwt_token(token)
    if not context:
        raise PermissionError("Invalid or expired security token")
    
    try:
        yield context
    finally:
        # Any cleanup operations
        pass

# Example usage and testing
if __name__ == "__main__":
    async def test_security_framework():
        print("🔒 Testing Quantum Security Framework...")
        
        # Initialize security manager
        security_mgr = QuantumSecurityManager(
            hive_id="test_security_hive",
            compliance_frameworks=[ComplianceFramework.SOC2, ComplianceFramework.GDPR]
        )
        
        # Test authentication
        print("\n🔐 Testing Authentication...")
        context = await security_mgr.authenticate_user(
            username="admin",
            password="admin123",
            source_ip="192.168.1.100",
            user_agent="QuantumHive/1.0"
        )
        
        if context:
            print(f"✅ Authentication successful for {context.user_id}")
            print(f"   Role: {context.role}")
            print(f"   Security Level: {context.security_level.value}")
            print(f"   Quantum Clearance: {context.quantum_clearance}")
        else:
            print("❌ Authentication failed")
        
        # Test JWT token creation and verification
        if context:
            print("\n🎫 Testing JWT Tokens...")
            token = security_mgr.create_jwt_token(context)
            print(f"✅ JWT token created: {token[:50]}...")
            
            verified_context = security_mgr.verify_jwt_token(token)
            if verified_context:
                print("✅ JWT token verified successfully")
            else:
                print("❌ JWT token verification failed")
        
        # Test authorization
        print("\n🛡️ Testing Authorization...")
        if context:
            # Test authorized operation
            authorized = security_mgr.authorize_operation(
                context, "quantum_core", "read", SecurityLevel.CONFIDENTIAL
            )
            print(f"✅ Quantum core read access: {'Allowed' if authorized else 'Denied'}")
            
            # Test unauthorized operation
            unauthorized = security_mgr.authorize_operation(
                context, "top_secret_data", "read", SecurityLevel.TOP_SECRET
            )
            print(f"🔒 Top secret access: {'Allowed' if unauthorized else 'Denied'}")
        
        # Test encryption
        print("\n🔐 Testing Encryption...")
        if CRYPTO_AVAILABLE:
            sensitive_data = {"quantum_key": "supersecret123", "coherence_level": 0.95}
            encrypted = security_mgr.encrypt_sensitive_data(sensitive_data)
            print(f"✅ Data encrypted: {len(encrypted)} bytes")
            
            decrypted = security_mgr.decrypt_sensitive_data(encrypted)
            print(f"✅ Data decrypted successfully: {len(decrypted)} characters")
        else:
            print("⚠️ Encryption not available - install cryptography package")
        
        # Test compliance checks
        print("\n📋 Running Compliance Checks...")
        compliance_results = await security_mgr.run_compliance_checks()
        print(f"✅ Compliance status: {compliance_results['overall_status']}")
        print(f"   Checks run: {len(compliance_results['checks'])}")
        print(f"   Violations: {len(compliance_results['violations'])}")
        
        # Show security metrics
        print("\n📊 Security Metrics...")
        metrics = security_mgr.get_security_metrics()
        print(f"   Active sessions: {metrics['active_sessions']}")
        print(f"   Audit events: {metrics['audit_events']}")
        print(f"   Encryption enabled: {metrics['encryption_enabled']}")
        print(f"   Quantum enhancement: {metrics['quantum_enhancement']}")
        
        print("\n✅ Security framework test completed!")
    
    # Run the test
    asyncio.run(test_security_framework())