# 🍽️ restaurante_app — Semana 15

**Estudiante:** Dayana Valeria Lema Saldaña  
**Asignatura:** Programación Orientada a Objetos — Universidad Estatal Amazónica  
**Entrega:** Semana 15 · Conceptos fundamentales de manejo de eventos

---

## 📌 ¿Qué cambia esta semana?

Esta entrega evoluciona `restaurante_app` (Sabor Verde) a partir de la gestión completa de platos construida en la Semana 14. El objetivo central es comprender los **fundamentos básicos del manejo de eventos**: cómo una acción del usuario sobre un componente (un botón) dispara, mediante `command=`, un **callback** que coordina una operación de negocio sin concentrar la lógica dentro de la interfaz.

Como contexto práctico se incorpora la sección **Ventas**, que relaciona un **cliente** existente con un **plato** existente y conserva el registro en `ventas.json`. Se conservan íntegramente el inicio de sesión, la navegación y la gestión completa de platos ya construidas.

---

## 🗂️ Estructura del proyecto

```
restaurante_app/
├── assets/
│   ├── icons/
│   └── logo/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```

No se modificó la organización heredada de la Semana 14; la evolución ocurre en `modelos/venta.py` (nuevo), `restaurante_servicio.py` (ampliado) y `ui/main_view.py` (nueva sección Ventas), además de incorporar la carpeta `assets/`, obligatoria esta semana.

---

## 🧩 Responsabilidad de cada capa

- `modelos/`: `Producto` (con indicador vegetariano), `Usuario` (con correo) y ahora `Venta`, que relaciona `usuario_identificacion`, `producto_codigo` y `fecha`, validados con `property`.
- `servicios/archivo_servicio.py`: lee y escribe los archivos JSON de `datos/`.
- `servicios/restaurante_servicio.py`: convierte los datos en objetos, valida el acceso y expone el CRUD completo de platos, además de `registrar_venta`, `listar_ventas`, `cantidad_ventas` y `guardar_ventas`. Toda la validación y persistencia de la venta vive aquí, no en la interfaz.
- `ui/`: `LoginView` y `MainView`, construidas con Tkinter, sin leer los archivos JSON directamente.
- `main.py`: crea la única ventana principal, configura el ícono del sistema desde `assets/` y controla el cambio entre vistas.

---

## 🥗 Sección Ventas: flujo de eventos aplicado

```
Cliente elige un Cliente y un Plato en los Combobox
                ↓
Clic en "Registrar venta"  (command=self.registrar_venta)
                ↓
Callback registrar_venta() en MainView:
    - obtiene el texto seleccionado en cada Combobox
    - lo traduce a la identificacion / codigo real
    - llama a restaurante_servicio.registrar_venta(...)
                ↓
RestauranteServicio.registrar_venta():
    - valida que ambos campos vengan seleccionados
    - valida que el cliente exista
    - valida que el plato exista
    - crea un objeto Venta (el modelo valida sus propios datos)
    - agrega la venta en memoria y llama a guardar_ventas()
                ↓
ArchivoServicio.escribir_json() persiste en ventas.json
                ↓
MainView.refrescar_ventas() actualiza la tabla (Treeview)
y la barra de estado inferior
```

El callback de la interfaz **no** decide si la venta es válida ni toca el archivo JSON: solo recolecta la selección y coordina la llamada al servicio, que concentra las reglas de negocio y la persistencia.

### Componentes usados en Ventas

- `ttk.Combobox` (solo lectura) para elegir un cliente y un plato existentes.
- `ttk.Button` con `command=self.registrar_venta`.
- `ttk.Treeview` + `ttk.Scrollbar` para las ventas registradas (Venta, Cliente, Plato, Fecha).
- `tk.LabelFrame` para separar el formulario del listado, igual que en Platos.

---

## 🖼️ Recursos gráficos (`assets/`)

Esta semana es obligatorio incorporar íconos y el logotipo del sistema:

- `assets/logo/logo.png`: logotipo mostrado en la pantalla de inicio de sesión.
- `assets/logo/icono.png`: versión simplificada usada como ícono de la ventana principal y junto al título en el encabezado.
- `assets/icons/`: íconos para cada botón de navegación (Inicio, Platos, Clientes, Ventas, Pedidos, Cerrar sesión) y para las acciones del formulario (Registrar, Consultar, Actualizar, Eliminar, Limpiar).

---

## 💾 Persistencia

Las ventas se guardan de inmediato en `datos/ventas.json` mediante `RestauranteServicio.guardar_ventas()`, que delega en `ArchivoServicio`. Al reabrir la aplicación, las ventas registradas se recuperan y se muestran en la tabla.

---

## ▶️ Flujo de la aplicación

```
Inicio -> LoginView -> RestauranteServicio valida el acceso -> MainView
MainView -> Inicio (resumen) | Clientes | Platos | Ventas
Ventas -> seleccionar cliente + plato -> Registrar venta
command= -> callback de venta -> RestauranteServicio valida y persiste
MainView -> Cerrar sesion -> LoginView
```

---

## 🔑 Credenciales de acceso (demostración)

| Usuario | Contraseña |
|---|---|
| `dlema` | `verde2026` |
| `admin` | `admin654` |

---

## ⚙️ Cómo ejecutar

```bash
cd restaurante_app
python main.py
```

---

## 🧪 Pruebas realizadas

- **Inicio de la aplicación:** `main.py` se ejecuta sin errores y muestra el ícono del sistema en la ventana.
- **Acceso correcto:** se despliega `MainView` con el logotipo en el encabezado.
- **Opción Platos:** el CRUD completo de la Semana 14 sigue funcionando sin cambios.
- **Opción Ventas:** muestra el formulario con los Combobox y la tabla de ventas.
- **Registrar venta:** con un cliente y un plato seleccionados, la venta aparece de inmediato en la tabla y se guarda en `ventas.json`.
- **Registrar venta sin selección:** `RestauranteServicio` rechaza la operación con un mensaje claro y no modifica `ventas.json`.
- **Reabrir la aplicación:** las ventas registradas se recuperan correctamente desde `ventas.json`.
- **Cierre de sesión:** regresa a `LoginView` sin abrir una ventana nueva.

---

## 📎 Nota educativa sobre autenticación

El acceso de esta etapa es una simulación con fines académicos; las contraseñas se guardan en JSON sin cifrado, lo cual no sería apropiado para un sistema en producción.
