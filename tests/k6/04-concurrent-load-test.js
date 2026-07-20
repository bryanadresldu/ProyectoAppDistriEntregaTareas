// Prueba 4: Usuarios concurrentes + distribucion de trafico entre nodos
// Uso: k6 run tests/k6/04-concurrent-load-test.js
//
// Cada respuesta incluye el header "X-App-Node" (agregado por el backend)
// que indica que nodo atendio la solicitud. Este script cuenta cuantas
// solicitudes atendio cada nodo para comprobar que NGINX respeta,
// aproximadamente, la proporcion de pesos configurada (5 / 3 / 2).
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter } from 'k6/metrics';

export const options = {
  scenarios: {
    concurrentUsers: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '10s', target: 20 },
        { duration: '30s', target: 20 },
        { duration: '10s', target: 0 }
      ]
    }
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<800']
  }
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost';

const node1Hits = new Counter('requests_app_node_1');
const node2Hits = new Counter('requests_app_node_2');
const node3Hits = new Counter('requests_app_node_3');

export default function () {
  const res = http.get(`${BASE_URL}/api/health`);

  check(res, { 'responde': (r) => r.status === 200 || r.status === 503 });

  const node = res.headers['X-App-Node'];
  if (node === 'app-node-1') node1Hits.add(1);
  else if (node === 'app-node-2') node2Hits.add(1);
  else if (node === 'app-node-3') node3Hits.add(1);

  sleep(0.5);
}

export function handleSummary(data) {
  const n1 = data.metrics.requests_app_node_1 ? data.metrics.requests_app_node_1.values.count : 0;
  const n2 = data.metrics.requests_app_node_2 ? data.metrics.requests_app_node_2.values.count : 0;
  const n3 = data.metrics.requests_app_node_3 ? data.metrics.requests_app_node_3.values.count : 0;
  const total = n1 + n2 + n3;

  const pct = (n) => (total ? ((n / total) * 100).toFixed(1) : '0.0');

  console.log('');
  console.log('=== Distribucion de trafico entre nodos (NGINX weighted) ===');
  console.log(`app-node-1: ${n1} solicitudes (${pct(n1)}%)  -> peso esperado 5/10 = 50%`);
  console.log(`app-node-2: ${n2} solicitudes (${pct(n2)}%)  -> peso esperado 3/10 = 30%`);
  console.log(`app-node-3: ${n3} solicitudes (${pct(n3)}%)  -> peso esperado 2/10 = 20%`);
  console.log(`total con header identificado: ${total}`);
  console.log('==============================================================');

  return {
    stdout: JSON.stringify(data, null, 2)
  };
}
