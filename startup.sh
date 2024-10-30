#!/bin/bash

set -euo pipefail

# Environment setup
source .env

# Project root directory
PROJECT_ROOT=$(pwd)

# Log file location
LOG_FILE="${PROJECT_ROOT}/logs/app.log"

# PID file locations
DATABASE_PID_FILE="${PROJECT_ROOT}/pids/database.pid"
BACKEND_PID_FILE="${PROJECT_ROOT}/pids/backend.pid"
FRONTEND_PID_FILE="${PROJECT_ROOT}/pids/frontend.pid"

# Service timeouts
DATABASE_TIMEOUT=30
BACKEND_TIMEOUT=60
FRONTEND_TIMEOUT=30

# Health check intervals
HEALTHCHECK_INTERVAL=2

# Function definitions
log_info() {
  timestamp=$(date +"%Y-%m-%d %H:%M:%S")
  echo "${timestamp} INFO: $*"
}

log_error() {
  timestamp=$(date +"%Y-%m-%d %H:%M:%S")
  echo "${timestamp} ERROR: $*" >&2
}

cleanup() {
  if [ -f "${DATABASE_PID_FILE}" ]; then
    kill $(cat "${DATABASE_PID_FILE}") 2>/dev/null
    rm "${DATABASE_PID_FILE}"
  fi
  if [ -f "${BACKEND_PID_FILE}" ]; then
    kill $(cat "${BACKEND_PID_FILE}") 2>/dev/null
    rm "${BACKEND_PID_FILE}"
  fi
  if [ -f "${FRONTEND_PID_FILE}" ]; then
    kill $(cat "${FRONTEND_PID_FILE}") 2>/dev/null
    rm "${FRONTEND_PID_FILE}"
  fi
}

check_dependencies() {
  log_info "Checking dependencies..."
  which python3 &>/dev/null || log_error "Python 3 not found. Please install Python 3."
  which pip &>/dev/null || log_error "Pip not found. Please install Pip."
  which uvicorn &>/dev/null || log_error "Uvicorn not found. Please install Uvicorn."
}

check_port() {
  port=$1
  if nc -z localhost ${port} 2>/dev/null; then
    log_info "Port ${port} is available."
    return 0
  else
    log_error "Port ${port} is not available."
    return 1
  fi
}

wait_for_service() {
  service=$1
  timeout=$2
  log_info "Waiting for ${service} to start..."
  start_time=$(date +%s)
  while true; do
    if check_port "${service}"; then
      log_info "${service} started successfully."
      return 0
    fi
    elapsed=$(($(date +%s) - ${start_time)))
    if [ ${elapsed} -ge ${timeout} ]; then
      log_error "${service} failed to start within timeout."
      return 1
    fi
    sleep ${HEALTHCHECK_INTERVAL}
  done
}

verify_service() {
  service=$1
  timeout=$2
  log_info "Verifying ${service} health..."
  start_time=$(date +%s)
  while true; do
    if check_port "${service}"; then
      log_info "${service} health check successful."
      return 0
    fi
    elapsed=$(($(date +%s) - ${start_time)))
    if [ ${elapsed} -ge ${timeout} ]; then
      log_error "${service} health check failed."
      return 1
    fi
    sleep ${HEALTHCHECK_INTERVAL}
  done
}

start_database() {
  log_info "Starting database..."
  nohup pg_ctl -D "${DATABASE_DATA_DIR}" start >"${LOG_FILE}" 2>&1 &
  store_pid "${DATABASE_PID_FILE}" "$!"
  wait_for_service "${DATABASE_PORT}" "${DATABASE_TIMEOUT}"
  verify_service "${DATABASE_PORT}" "${DATABASE_TIMEOUT}"
}

start_backend() {
  log_info "Starting backend server..."
  nohup uvicorn main:app --host 0.0.0.0 --port ${BACKEND_PORT} >"${LOG_FILE}" 2>&1 &
  store_pid "${BACKEND_PID_FILE}" "$!"
  wait_for_service "${BACKEND_PORT}" "${BACKEND_TIMEOUT}"
  verify_service "${BACKEND_PORT}" "${BACKEND_TIMEOUT}"
}

start_frontend() {
  log_info "Starting frontend server..."
  nohup npm run start >"${LOG_FILE}" 2>&1 &
  store_pid "${FRONTEND_PID_FILE}" "$!"
  wait_for_service "${FRONTEND_PORT}" "${FRONTEND_TIMEOUT}"
  verify_service "${FRONTEND_PORT}" "${FRONTEND_TIMEOUT}"
}

store_pid() {
  pid_file=$1
  pid=$2
  echo "${pid}" >"${pid_file}"
  log_info "Stored process ID to ${pid_file}"
}

trap cleanup EXIT ERR

# Main execution flow
check_dependencies
start_database
start_backend
start_frontend

log_info "Services started successfully."

echo "Backend API available at http://localhost:${BACKEND_PORT}"
echo "Frontend available at http://localhost:${FRONTEND_PORT}"