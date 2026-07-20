// Prueba 2: Login de estudiante
// Uso: k6 run tests/k6/02-login-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 3,
  duration: '15s'
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost';

const CREDENTIALS = {
  email: 'ana.torres@epn.edu.ec',
  password: 'Estudiante123!'
};

export default function () {
  const res = http.post(`${BASE_URL}/api/auth/login`, JSON.stringify(CREDENTIALS), {
    headers: { 'Content-Type': 'application/json' }
  });

  check(res, {
    'login responde 200': (r) => r.status === 200,
    'login devuelve token': (r) => {
      try {
        return Boolean(JSON.parse(r.body).token);
      } catch (e) {
        return false;
      }
    },
    'header X-App-Node presente': (r) => r.headers['X-App-Node'] !== undefined
  });

  sleep(1);
}
