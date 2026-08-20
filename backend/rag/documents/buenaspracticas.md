# Google Ads - Buenas Prácticas

## Reglas Generales:
* Modelo de atribución recomendado: `GOOGLE_SEARCH_ATTRIBUTION_DATA_DRIVEN` debe emplearse en todas las conversiones principales.
* Modelos obsoletos: `GOOGLE_SEARCH_ATTRIBUTION_FIRST_CLICK`, `GOOGLE_SEARCH_ATTRIBUTION_LINEAR`, `GOOGLE_SEARCH_ATTRIBUTION_TIME_DECAY` y `GOOGLE_SEARCH_ATTRIBUTION_POSITION_BASED`.
* Optimización de Smart Bidding: Toda conversión principal de negocio debe tener `primary_for_goal = true`. Si está en `false`, el algoritmo de pujas no optimizará para conseguirla.

---

## Category: PURCHASE
* Propósito: Medición de transacciones económicas directas en el sitio web o aplicación.
* Counting Type: `MANY_PER_CLICK`. Si un usuario realiza 3 compras tras un solo clic, se deben contabilizar los 3 ingresos.
* Primary for Goal: `true`.
* Ventana Post-Clic: Entre `30` y `60` días (según el periodo de decisión del producto).

---

## Category: SUBMIT_LEAD_FORM
* Propósito: Captura de clientes potenciales mediante el envío de formularios de solicitud o presupuesto.
* Counting Type: `ONE_PER_CLICK`. Si un usuario reenvía el formulario varias veces por error, solo debe contar 1 lead. 
* Primary for Goal: `true`.
* Ventana Post-Clic:** Entre `30` y `90` días (adaptada al ciclo de maduración de clientes B2B). Ventanas inferiores a `14` días se consideran ADVERTENCIA.

---

## Category: PHONE_CALL_LEAD
* Propósito: Registro de llamadas telefónicas iniciadas desde el sitio web o anuncios (ej. cerrajerías, grúas, clínicas).
* Counting Type:** `ONE_PER_CLICK`. Reintentos o llamadas continuadas de un mismo cliente corresponden a la misma oportunidad comercial.
* Primary for Goal: `true`.
* Ventana Post-Clic: Entre `7` y `14` días (por la inmediatez de la necesidad del servicio). Ventanas superiores a `30` días se consideran ADVERTENCIA.