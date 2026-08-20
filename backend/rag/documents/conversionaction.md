# Google Ads API - Conversion Action

## Conversion Action - Definición
Representa una acción de conversión individual dentro de una cuenta de Google Ads. Describe el evento que el usuario realiza tras interactuar con un anuncio (comprar, rellenar formulario, llamar, ect) y contiene la configuración técnica, comercial y de atribución empleada para optimizar las campañas y medir el rendimiento.

---

## Campo: conversion_action.resource_name
* Descripción: Nombre del recurso inmutable que identifica unívocamente la acción de conversión dentro de la API de Google Ads.
* Tipo de dato: STRING
* Formato: customers/{customer_id}/conversionActions/{conversion_action_id}

---

## Campo: conversion_action.id
* Descripción: Identificador numérico único asignado a la acción de conversión.
* Tipo de dato: INT64

---

## Campo: conversion_action.name
* Descripción: Nombre descriptivo visible de la acción de conversión en los informes y en la interfaz. Debe ser único dentro de la cuenta (incluso respecto a conversiones en estado REMOVED).
* Tipo de dato: STRING

---

## Campo: conversion_action.category
* Descripción: La categoría funcional o el propósito de negocio que representa la acción de conversión.
* Tipo de dato: ENUM (ConversionActionCategory)
* Opciones:
    * PURCHASE: Compra completada.
    * SUBMIT_LEAD_FORM: Formulario de contacto.
    * PHONE_CALL_LEAD: Llamada telefónica de cliente potencial.
    * SIGN_UP: Registro de usuario, suscripción o creación de cuenta.
    * PAGE_VIEW: Visualización de una página web.
    * DOWNLOAD: Descarga de un recurso o archivo.
    * DEFAULT: Categoría genérica no especificada.

---

## Campo: conversion_action.type
* Descripción: : El tipo o la fuente técnica a través de la cual se origina el evento de conversión.
* Tipo de dato: ENUM (ConversionActionType)
* Opciones:
    * WEBPAGE: Eventos capturados directamente en el sitio web mediante etiqueta de Google o GTM.
    * PHONE_CALL_LEAD: Llamadas telefónicas desde un número mostrado en el sitio web.
    * CLICK_TO_CALL: Llamadas iniciadas directamente desde la extensión de llamada del anuncio.
    * GOOGLE_ANALYTICS_4: Conversiones importadas desde una propiedad vinculada de GA4.
    * UPLOAD_CLICKS: Conversiones offline importadas mediante archivo o CRM.

---

## Campo: conversion_action.status
* Descripción: El estado administrativo actual de la acción de conversión en la cuenta.
* Tipo de dato: ENUM (ConversionActionStatus)
* Opciones:
    * ENABLED: La conversión está activa y recopilando datos.
    * PAUSED: La conversión está pausada.
    * REMOVED: La conversión ha sido eliminada lógicamente.
    * HIDDEN: Oculta en la interfaz por el sistema.

---

## Campo: conversion_action.counting_type
* Descripcion: Define cómo se contabilizan las conversiones que se producen a partir de un mismo clic.
* Tipo de dato: ENUM (ConversionActionCountingType)
* Opciones:
    * MANY_PER_CLICK: Registra todas las conversiones ocurridas tras un mismo clic (recomendado para ventas/compras).
    * ONE_PER_CLICK: Registra como máximo 1 conversión por cada clic, ignorando las repeticiones del mismo usuario (recomendado para leads/formularios).

---

## Campo: conversion_action.primary_for_goal
* Descripción: Indica si la acción de conversión se utiliza de forma primaria para optimizar las estrategias de puja automática (Smart Bidding).
* Tipo de dato: BOOLEAN
* Opciones:
    * true: Conversión principal. El algoritmo orienta las pujas para maximizar esta acción.
    * false: Conversión secundaria. Se registra únicamente para informes; el algoritmo de puja la ignora.

---

## Campo: conversion_action.click_through_lookback_window_days
* Descripción: Período (en días) posterior al clic en un anuncio dentro del cual se registrará y atribuirá una conversión si el usuario la realiza.
* Tipo de dato: INT64 (Rango válido: entre 1 y 90 días)

---

## Campo: conversion_action.attribution_model_settings.attribution_model
* Descripción: El modelo utilizado para distribuir el crédito de la conversión entre las distintas interacciones del usuario.
* Tipo de dato: ENUM (AttributionModel)
* Opciones:
    * GOOGLE_SEARCH_ATTRIBUTION_DATA_DRIVEN: Modelo basado en datos (Data-Driven) mediante IA.
    * GOOGLE_ADS_LAST_CLICK: Atribución de último clic.
    * GOOGLE_SEARCH_ATTRIBUTION_FIRST_CLICK: Primer clic (Obsoleto / Legacy).
    * GOOGLE_SEARCH_ATTRIBUTION_LINEAR: Lineal (Obsoleto / Legacy).
    * GOOGLE_SEARCH_ATTRIBUTION_TIME_DECAY: Declive en el tiempo (Obsoleto / Legacy).
    * GOOGLE_SEARCH_ATTRIBUTION_POSITION_BASED: Según la posición (Obsoleto / Legacy).

---

## Campo: conversion_action.attribution_model_settings.data_driven_model_status
* Descripción: Estado de disponibilidad del modelo basado en datos (Data-Driven) para esta acción de conversión específica.
* Tipo de dato: ENUM (DataDrivenModelStatus)
* Opciones:
    * AVAILABLE: El modelo basado en datos está activo y disponible.
    * STALE: El modelo se ha degradado por falta de volumen de datos reciente.
    * EXPIRED: El modelo ha expirado debido a un periodo prolongado sin suficiente volumen de conversiones.
    * NEVER_ELIGIBLE: La conversión no reúne las condiciones mínimas para usar atribución basada en datos.
    * UNKNOWN / UNSPECIFIED: Estado no determinado.