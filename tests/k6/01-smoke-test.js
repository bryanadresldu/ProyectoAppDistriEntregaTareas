// Prueba 1: Acceso basico al sistema (smoke test)
// Uso: k6 run tests/k6/01-smoke-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 1,
  iterations: 5
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost';

export default function () {
  const res = http.get(`${BASE_URL}/`);

  check(res, {
    'status es 200': (r) => r.status === 200,
    'contiene el frontend HTML': (r) => r.body.includes('Mesa de Entregas')
  });

  const apiHealth = http.get(`${BASE_URL}/api/health`);
  check(apiHealth, {
    'API /health responde': (r) => r.status === 200 || r.status === 503
  });

  sleep(1);
}
