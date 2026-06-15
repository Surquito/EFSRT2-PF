# Sistema de Evaluación de Desempeño de Empleados
**FinSupport Contact Center**

Aplicación de escritorio desarrollada en **Python** orientada a la gestión, análisis y visualización del desempeño del talento humano en entornos de **call center financiero**.

---

## Descripción del Proyecto

Este sistema permite **centralizar y automatizar el proceso de evaluación de desempeño**, integrando el registro de métricas, cálculo de indicadores clave (KPIs) y visualización mediante dashboards interactivos.

La solución responde a necesidades reales del área de **Recursos Humanos y gestión operativa**, facilitando la toma de decisiones basada en datos.

---

## Funcionalidades Principales

### Gestión de Empleados
- Registro y administración de colaboradores
- Organización por áreas funcionales

---

### Evaluación de Desempeño
- Registro de métricas por periodo (Año / Mes)
- Visualización de evaluaciones individuales
- Cálculo automático de promedios
- Registro de comentarios cualitativos

---

### Carga Masiva de Evaluaciones
- Importación de datos desde archivos Excel (.xlsx)
- Procesamiento estructurado de información
- Carga automática a base de datos
- Historial de procesos realizados

---

### Dashboard de Análisis
- Ranking de empleados (Top desempeño)
- Comparación de desempeño por área
- Evolución del rendimiento en el tiempo
- Distribución del desempeño (alto, medio, bajo)

---

## Arquitectura del Sistema

El proyecto está diseñado bajo un enfoque modular basado en principios similares al patrón **MVC (Modelo – Vista – Servicios)**:

FinSupport/
│
├── database/        → Conexión a base de datos (PostgreSQL - Supabase)
├── models/          → Definición de entidades (POO)
├── services/        → Lógica de negocio y acceso a datos
├── views/           → Interfaz gráfica (Tkinter)
├── utils/           → Funciones auxiliares reutilizables
├── img/             → Recursos visuales
│
├── main.py          → Punto de entrada de la aplicación
├── .env             → Variables de entorno
├── requirements.txt → Dependencias


---

## Tecnologías Utilizadas

- **Python 3**
- **Tkinter** → Interfaz gráfica de usuario
- **Matplotlib** → Visualización de datos
- **PostgreSQL (Supabase)** → Base de datos en la nube
- **Psycopg2** → Conexión a base de datos
- **Pandas** → Procesamiento de datos

---

## Enfoque de Negocio

El sistema está diseñado considerando métricas clave en call centers financieros:

- AHT (Tiempo promedio de atención)
- FCR (Resolución en primera llamada)
- CSAT (Satisfacción del cliente)
- Calidad de atención
- Adherencia operativa

---

## Beneficios del Sistema

- Automatización de evaluaciones de desempeño  
- Centralización de información  
- Visualización clara mediante dashboards  
- Soporte para toma de decisiones basada en datos  
- Arquitectura escalable y mantenible  

---

## Ejecución del Proyecto

```bash
pip install -r requirements.txt
python main.py
