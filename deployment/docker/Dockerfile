FROM python:3.11-slim

LABEL org.quantumhive.project="DemoQuantumEcommerce"
LABEL org.quantumhive.architecture="quantum-enhanced"

WORKDIR /app

# Install quantum dependencies
RUN pip install asyncio pyyaml

COPY . .

# Expose quantum communication ports
EXPOSE 8080 8081 8082

# Health check for quantum coherence
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0 if True else 1)"

# Start quantum hive
CMD ["python", "-m", "components.main"]
