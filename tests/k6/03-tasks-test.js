// Prueba 3: Consulta de tareas (requiere autenticacion previa)
// Uso: k6 run tests/k6/03-tasks-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 5,
  duration: '20s'
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost';

const CREDENTIALS = {
  email: 'luis.andrade@epn.edu.ec',
  password: 'Estudiante123!'
};

export function setup() {
  const res = http.post(`${BASE_URL}/api/auth/login`, JSON.stringify(CREDENTIALS), {
    headers: { 'Content-Type': 'application/json' }
  });
  const token = JSON.parse(res.body).token;
  return { token };
}

export default function (data) {
  const res = http.get(`${BASE_URL}/api/tasks`, {
    headers: { Authorization: `Bearer ${data.token}` }
  });

  check(res, {
    'consulta de tareas responde 200': (r) => r.status === 200,
    'devuelve un arreglo de tareas': (r) => {
      try {
        return Array.isArray(JSON.parse(r.body).tasks);
      } catch (e) {
        return false;
      }
    }
  });

  sleep(1);
}
