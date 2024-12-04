import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '1m', target: 50 }, // 50 usuarios simultáneos
        { duration: '3m', target: 500 }, // Incrementar a 100 usuarios
        { duration: '1m', target: 0 },  // Finalizar prueba
    ],
    thresholds: {
        http_req_duration: ['p(95)<2000'], // 95% de las solicitudes deben responder en menos de 2s
    },
};

export default function () {
    const url = 'http://localhost:80/jwt/generate';
    const payload = JSON.stringify({ "payload": { "user_id": 1 }, "expiration_minutes": 10 });
    const params = { headers: { 'Content-Type': 'application/json' } };

    const res = http.post(url, payload, params);
    check(res, {
        'status is 200': (r) => r.status === 200,
        'response time is below 2s': (r) => r.timings.duration < 2000,
    });
    sleep(1);
}