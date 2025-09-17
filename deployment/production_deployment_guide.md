# Quantum Hive Production Deployment Guide

## 🚀 Complete Enterprise Deployment Framework

This guide provides step-by-step instructions for deploying the Quantum Hive architecture in production environments with full enterprise features including monitoring, security, compliance, and scaling.

## 📋 Prerequisites

### System Requirements
- **CPU**: 8+ cores recommended
- **RAM**: 16GB+ recommended
- **Storage**: 100GB+ SSD recommended
- **OS**: Linux (Ubuntu 20.04+ recommended)

### Software Dependencies
- Docker 20.10+
- Docker Compose 2.0+
- Kubernetes 1.25+ (for K8s deployment)
- Git

### Network Requirements
- Ports 80, 443 (HTTP/HTTPS)
- Port 8080 (Quantum Hive API)
- Port 3000 (Grafana)
- Port 9090-9093 (Metrics/Monitoring)
- Port 5601 (Kibana)

## 🔧 Installation Steps

### 1. Clone and Setup

```bash
# Clone the repository
git clone <quantum-hive-repo>
cd quantum-hive

# Create production directories
mkdir -p deployment/secrets
mkdir -p deployment/ssl
mkdir -p deployment/logs
mkdir -p deployment/data
```

### 2. Configure Secrets

Create secure passwords for all services:

```bash
# Generate secure passwords
openssl rand -base64 32 > deployment/secrets/postgres_password.txt
openssl rand -base64 32 > deployment/secrets/redis_password.txt
openssl rand -base64 32 > deployment/secrets/grafana_password.txt
openssl rand -base64 32 > deployment/secrets/rabbitmq_password.txt

# Set proper permissions
chmod 600 deployment/secrets/*
```

### 3. SSL/TLS Configuration

```bash
# Generate self-signed certificates (replace with real certs in production)
cd deployment/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout quantum-hive.key \
    -out quantum-hive.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=quantum-hive.yourdomain.com"
```

### 4. Environment Configuration

Create production environment file:

```bash
# deployment/.env.production
HIVE_ID=prod_hive_$(date +%s)
QUANTUM_COHERENCE_TARGET=0.95
CONSCIOUSNESS_LEVEL_TARGET=4
EVOLUTIONARY_ADAPTATION=true
ENABLE_QUANTUM_ENCRYPTION=true
COMPLIANCE_FRAMEWORKS=SOC2,GDPR
LOG_LEVEL=INFO
METRICS_RETENTION_DAYS=90
```

### 5. Deploy with Docker Compose

```bash
# Start the complete production stack
docker-compose -f deployment/docker-compose.production.yaml up -d

# Check service health
docker-compose -f deployment/docker-compose.production.yaml ps
```

### 6. Verify Deployment

```bash
# Check Quantum Hive API
curl -f http://localhost:8080/health

# Check Prometheus metrics
curl -f http://localhost:9092/metrics

# Check Grafana (admin / <grafana_password>)
open http://localhost:3000

# Check Kibana logs
open http://localhost:5601
```

## 🐳 Kubernetes Deployment

### 1. Deploy to Kubernetes

```bash
# Apply all Kubernetes manifests
kubectl apply -f deployment/k8s/

# Check deployment status
kubectl get pods -n quantum-hive
kubectl get services -n quantum-hive
```

### 2. Configure Ingress

```bash
# Update ingress with your domain
sed -i 's/quantum-hive.yourdomain.com/your-actual-domain.com/g' \
    deployment/k8s/quantum-hive-services.yaml

# Apply updated configuration
kubectl apply -f deployment/k8s/quantum-hive-services.yaml
```

### 3. Scale Services

```bash
# Scale quantum core replicas
kubectl scale deployment quantum-hive-core --replicas=5 -n quantum-hive

# Scale genetic workers
kubectl scale deployment quantum-genetic-workers --replicas=3 -n quantum-hive
```

## 📊 Monitoring & Observability

### Grafana Dashboards

1. **Quantum Hive Overview**: Real-time quantum metrics, consciousness levels
2. **Genetic Programming**: Evolution tracking, fitness scores
3. **Chemical Bonds**: Bond formation/dissolution monitoring
4. **System Health**: Resource utilization, performance metrics

### Key Metrics to Monitor

- **Quantum Coherence**: Target >90%
- **Consciousness Level**: Progressive evolution
- **Genetic Fitness**: Upward trending
- **Chemical Bonds**: Stability >3.0
- **API Latency**: <100ms p95
- **Error Rate**: <1%

### Alerting Rules

```yaml
# Critical Alerts
- Quantum Coherence < 70%
- Consciousness Regression
- High Error Rate > 5%
- Resource Exhaustion > 90%
- Security Violations

# Warning Alerts  
- Genetic Fitness Decline
- Chemical Bond Weakening
- High API Latency
- Disk Space < 20%
```

## 🔒 Security Configuration

### 1. Authentication Setup

```bash
# Configure OAuth2 (example with Auth0)
export OAUTH_CLIENT_ID="your-client-id"
export OAUTH_CLIENT_SECRET="your-client-secret"
export OAUTH_DOMAIN="your-tenant.auth0.com"
```

### 2. Compliance Checks

```bash
# Run automated compliance scan
python -m deployment.security.quantum_security_framework

# Review compliance dashboard
open http://localhost:3000/d/compliance
```

### 3. Security Hardening

- Enable firewall (UFW/iptables)
- Configure fail2ban for intrusion detection
- Implement log rotation
- Enable audit logging
- Regular security updates

## 🔄 Backup & Disaster Recovery

### Database Backups

```bash
# Automated PostgreSQL backup
docker exec quantum-postgres pg_dump -U quantum_admin quantum_hive > \
    /backup/quantum_hive_$(date +%Y%m%d_%H%M%S).sql

# Redis backup
docker exec quantum-redis redis-cli --rdb /data/dump.rdb
```

### Configuration Backups

```bash
# Backup all configuration
tar -czf quantum_hive_config_$(date +%Y%m%d).tar.gz \
    deployment/k8s/ \
    deployment/monitoring/ \
    deployment/security/ \
    quantum-hive.yaml
```

## 📈 Scaling Guidelines

### Horizontal Scaling Triggers

- **CPU Usage** > 70% for 5+ minutes
- **Memory Usage** > 80% for 5+ minutes  
- **Queue Length** > 1000 messages
- **API Response Time** > 500ms p95

### Scaling Configuration

```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: quantum-hive-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: quantum-hive-core
  minReplicas: 3
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## 🚨 Troubleshooting

### Common Issues

#### Quantum Coherence Degradation
```bash
# Check quantum workers
kubectl logs -l app=quantum-hive,component=genetic-worker -n quantum-hive

# Restart quantum core
kubectl rollout restart deployment/quantum-hive-core -n quantum-hive
```

#### Memory Leaks
```bash
# Monitor memory usage
docker stats quantum-hive-core

# Check for memory leaks in logs
grep "OutOfMemory\|MemoryError" deployment/logs/*.log
```

#### Database Connection Issues
```bash
# Check PostgreSQL health
kubectl exec -it postgres-0 -n quantum-hive -- pg_isready

# Check connection pool
kubectl logs quantum-hive-core -n quantum-hive | grep "connection"
```

## 📞 Support & Maintenance

### Regular Maintenance Tasks

**Daily:**
- Check service health
- Review error logs
- Monitor resource usage

**Weekly:**
- Update security patches
- Review compliance reports
- Analyze performance trends

**Monthly:**
- Full backup verification
- Security audit
- Capacity planning review

### Performance Optimization

1. **Database Tuning**: Optimize PostgreSQL settings
2. **Caching Strategy**: Implement Redis caching
3. **Load Balancing**: Configure NGINX upstream
4. **CDN Integration**: Static asset distribution

## 🏆 Production Checklist

- [ ] All services healthy and responding
- [ ] SSL/TLS certificates configured
- [ ] Authentication and authorization working
- [ ] Monitoring dashboards operational
- [ ] Alerting rules configured and tested
- [ ] Backup strategy implemented
- [ ] Security hardening completed
- [ ] Compliance checks passing
- [ ] Documentation updated
- [ ] Team training completed

## 📚 Additional Resources

- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/)
- [Prometheus Monitoring](https://prometheus.io/docs/)
- [Security Hardening Guide](./security/README.md)
- [Compliance Framework](./compliance/README.md)
- [API Documentation](./api/README.md)

---

🧬 **Quantum Hive Production Deployment - Ready for Enterprise Scale**

For support, please contact: quantum-hive-support@yourdomain.com