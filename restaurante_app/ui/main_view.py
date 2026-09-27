import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from modelos.producto import Producto


class MainView(tk.Frame):
    def __init__(self, master, restaurante_servicio, usuario_actual, al_cerrar_sesion):
        super().__init__(master, bg="#f1f8f2")
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion

        self.contenido = None
        self.etiqueta_estado = None
        self.botones_menu = {}
        self.iconos = {}
        self.logo_encabezado = None

        self.producto_codigo_entry = None
        self.producto_nombre_entry = None
        self.producto_precio_entry = None
        self.producto_categoria_combo = None
        self.producto_vegetariano_var = None
        self.producto_stock_spin = None
        self.tabla_productos = None
        self.tabla_usuarios = None

        self.usuario_venta_combo = None
        self.producto_venta_combo = None
        self.tabla_ventas = None
        self.opciones_usuarios_venta = {}
        self.opciones_productos_venta = {}

        self.definir_estilos()
        self.construir_interfaz()

    # -------------------------------------------------------------------
    # Carga de recursos graficos desde la carpeta assets/ del proyecto.
    # -------------------------------------------------------------------
    def cargar_icono(self, nombre_archivo):
        if nombre_archivo in self.iconos:
            return self.iconos[nombre_archivo]

        ruta_base = Path(__file__).resolve().parent.parent
        ruta_icono = ruta_base / "assets" / "icons" / nombre_archivo

        if not ruta_icono.exists():
            return None

        icono = tk.PhotoImage(file=str(ruta_icono))
        self.iconos[nombre_archivo] = icono
        return icono

    def cargar_logo_encabezado(self):
        ruta_base = Path(__file__).resolve().parent.parent
        ruta_logo = ruta_base / "assets" / "logo" / "icono.png"

        if not ruta_logo.exists():
            return None

        self.logo_encabezado = tk.PhotoImage(file=str(ruta_logo))
        return self.logo_encabezado

    def crear_boton_con_icono(self, contenedor, texto, comando, estilo, icono=None):
        imagen = self.cargar_icono(icono) if icono else None

        if imagen is not None:
            return ttk.Button(
                contenedor,
                text=texto,
                command=comando,
                style=estilo,
                image=imagen,
                compound="left",
            )
        return ttk.Button(contenedor, text=texto, command=comando, style=estilo)

    # -------------------------------------------------------------------
    # Colores y estilos reutilizables de la vista principal.
    # -------------------------------------------------------------------
    def definir_estilos(self):
        self.color_fondo = "#f1f8f2"
        self.color_panel = "#ffffff"
        self.color_encabezado = "#1b4d20"
        self.color_texto = "#264d29"
        self.color_secundario = "#c8e6c9"
        self.color_resaltado = "#2e7d32"

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "MenuApp.TButton",
            background=self.color_secundario,
            foreground=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padding=(12, 8),
            borderwidth=0,
        )
        estilo.map("MenuApp.TButton", background=[("active", "#a9d5ab")])
        estilo.configure(
            "MenuActivo.TButton",
            background=self.color_resaltado,
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(12, 8),
            borderwidth=0,
        )
        estilo.map("MenuActivo.TButton", background=[("active", "#256428")])
        estilo.configure(
            "CerrarSesion.TButton",
            background="#8b3a1f",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(12, 8),
            borderwidth=0,
        )
        estilo.map("CerrarSesion.TButton", background=[("active", "#6f2e18")])
        estilo.configure(
            "Accion.TButton",
            background=self.color_resaltado,
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )
        estilo.map("Accion.TButton", background=[("active", "#256428")])
        estilo.configure(
            "Secundario.TButton",
            background="#5c7a5e",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )
        estilo.map("Secundario.TButton", background=[("active", "#48604a")])
        estilo.configure(
            "Eliminar.TButton",
            background="#8b3a1f",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(10, 7),
            borderwidth=0,
        )
        estilo.map("Eliminar.TButton", background=[("active", "#6f2e18")])
        estilo.configure(
            "Treeview.Heading",
            background=self.color_secundario,
            foreground=self.color_encabezado,
            font=("Arial", 10, "bold"),
        )
        estilo.configure("Treeview", rowheight=24, font=("Arial", 10))
        estilo.configure(
            "Vegetariano.TCheckbutton",
            background=self.color_panel,
            foreground=self.color_texto,
            font=("Arial", 10),
        )

    # -------------------------------------------------------------------
    # Estructura principal: encabezado, navegacion, contenido y estado.
    # -------------------------------------------------------------------
    def construir_interfaz(self):
        encabezado = tk.Frame(self, bg=self.color_encabezado, padx=28, pady=14)
        encabezado.pack(fill="x")

        bloque_titulo = tk.Frame(encabezado, bg=self.color_encabezado)
        bloque_titulo.pack(anchor="w")

        logo = self.cargar_logo_encabezado()
        if logo is not None:
            tk.Label(bloque_titulo, image=logo, bg=self.color_encabezado).pack(
                side="left", padx=(0, 12)
            )

        bloque_texto = tk.Frame(bloque_titulo, bg=self.color_encabezado)
        bloque_texto.pack(side="left")

        tk.Label(
            bloque_texto,
            text="🍽️ SABOR VERDE",
            bg=self.color_encabezado,
            fg="#ffffff",
            font=("Arial", 19, "bold"),
        ).pack(anchor="w")

        tk.Label(
            bloque_texto,
            text=f"Bienvenido, {self.usuario_actual.nombre}",
            bg=self.color_encabezado,
            fg="#c8e6c9",
            font=("Arial", 11),
        ).pack(anchor="w", pady=(4, 0))

        barra = tk.Frame(self, bg=self.color_secundario, padx=18, pady=10)
        barra.pack(fill="x")

        self.crear_boton_menu(barra, "Inicio", self.mostrar_inicio, "home.png")
        self.crear_boton_menu(barra, "Platos", self.mostrar_productos, "productos.png")
        self.crear_boton_menu(barra, "Clientes", self.mostrar_usuarios, "users.png")
        self.crear_boton_menu(barra, "Ventas", self.mostrar_ventas, "ventas.png")
        self.crear_boton_menu(barra, "Pedidos", self.mostrar_funcionalidad_pendiente, "pedidos.png")

        self.crear_boton_con_icono(
            barra,
            "Cerrar sesion",
            self.cerrar_sesion,
            "CerrarSesion.TButton",
            "logout.png",
        ).pack(side="right")

        self.contenido = tk.Frame(self, bg=self.color_fondo, padx=28, pady=22)
        self.contenido.pack(fill="both", expand=True)

        self.crear_barra_estado()
        self.mostrar_inicio()

    def crear_boton_menu(self, contenedor, texto, comando, icono=None):
        boton = self.crear_boton_con_icono(contenedor, texto, comando, "MenuApp.TButton", icono)
        boton.pack(side="left", padx=(0, 8))
        self.botones_menu[texto] = boton

    def marcar_seccion(self, seccion):
        for texto, boton in self.botones_menu.items():
            estilo = "MenuActivo.TButton" if texto == seccion else "MenuApp.TButton"
            boton.configure(style=estilo)

    def limpiar_contenido(self):
        assert self.contenido is not None

        for widget in self.contenido.winfo_children():
            widget.destroy()

    def crear_barra_estado(self):
        barra_estado = tk.Frame(self, bg=self.color_secundario, padx=18, pady=8)
        barra_estado.pack(fill="x", side="bottom")

        self.etiqueta_estado = tk.Label(
            barra_estado,
            bg=self.color_secundario,
            fg=self.color_texto,
            font=("Arial", 10),
        )
        self.etiqueta_estado.pack(side="left")
        self.actualizar_barra_estado()

    def actualizar_barra_estado(self):
        assert self.etiqueta_estado is not None

        self.etiqueta_estado.config(
            text=(
                f"Platos: {self.restaurante_servicio.cantidad_productos()} | "
                f"Clientes: {self.restaurante_servicio.cantidad_usuarios()} | "
                f"Ventas: {self.restaurante_servicio.cantidad_ventas()} | "
                "Informacion cargada desde JSON"
            )
        )

    # -------------------------------------------------------------------
    # Seccion Inicio: resumen general del panel principal.
    # -------------------------------------------------------------------
    def mostrar_inicio(self):
        self.marcar_seccion("Inicio")
        self.limpiar_contenido()
        self.actualizar_barra_estado()

        assert self.contenido is not None

        tk.Label(
            self.contenido,
            text="Panel principal",
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 18, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            self.contenido,
            text="Consulte los clientes registrados y gestione el menu saludable "
            "desde las opciones superiores.",
            bg=self.color_fondo,
            fg=self.color_texto,
            font=("Arial", 12),
        ).pack(anchor="w", pady=(0, 22))

        resumen = tk.Frame(self.contenido, bg=self.color_fondo)
        resumen.pack(fill="x")

        self.crear_tarjeta_resumen(
            resumen, "Platos disponibles", self.restaurante_servicio.cantidad_productos()
        )
        self.crear_tarjeta_resumen(
            resumen, "Clientes registrados", self.restaurante_servicio.cantidad_usuarios()
        )
        self.crear_tarjeta_resumen(
            resumen, "Ventas registradas", self.restaurante_servicio.cantidad_ventas()
        )

    def crear_tarjeta_resumen(self, contenedor, titulo, valor):
        tarjeta = tk.Frame(contenedor, bg=self.color_panel, padx=18, pady=16)
        tarjeta.pack(side="left", fill="x", expand=True, padx=(0, 14))

        tk.Label(
            tarjeta,
            text=titulo,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).pack(anchor="w")
        tk.Label(
            tarjeta,
            text=str(valor),
            bg=self.color_panel,
            fg=self.color_resaltado,
            font=("Arial", 24, "bold"),
        ).pack(anchor="w", pady=(8, 0))

    # -------------------------------------------------------------------
    # Seccion Clientes: consulta mediante tabla (solo lectura).
    # -------------------------------------------------------------------
    def mostrar_usuarios(self):
        self.marcar_seccion("Clientes")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Clientes registrados")
        listado = self.crear_panel_listado(self.contenido, "Consulta de clientes")
        self.tabla_usuarios = self.crear_tabla(
            listado,
            ("identificacion", "nombre", "correo", "usuario"),
            ("Identificacion", "Nombre", "Correo", "Usuario"),
            anchos=(105, 150, 190, 100),
        )
        self.refrescar_usuarios()

    def refrescar_usuarios(self):
        assert self.tabla_usuarios is not None

        self.limpiar_tabla(self.tabla_usuarios)
        for usuario in self.restaurante_servicio.listar_usuarios():
            self.tabla_usuarios.insert(
                "",
                tk.END,
                values=(usuario.identificacion, usuario.nombre, usuario.correo, usuario.usuario),
            )

        self.actualizar_barra_estado()

    # -------------------------------------------------------------------
    # Seccion Platos: formulario + tabla + operaciones CRUD.
    # -------------------------------------------------------------------
    def mostrar_productos(self):
        self.marcar_seccion("Platos")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Gestion de platos")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(
            cuerpo,
            text="Datos del plato",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=14,
            pady=14,
        )
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        self.producto_codigo_entry = self.crear_campo(formulario, "Codigo", 0)
        self.producto_nombre_entry = self.crear_campo(formulario, "Nombre", 1)
        self.producto_precio_entry = self.crear_campo(formulario, "Precio", 2)
        self.producto_categoria_combo = self.crear_campo_categoria(formulario, "Categoria", 3)
        self.producto_vegetariano_var = self.crear_campo_vegetariano(formulario, 4)
        self.producto_stock_spin = self.crear_campo_stock(formulario, "Stock", 5)

        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        botones = (
            ("Registrar", self.registrar_producto, "Accion.TButton", "add.png"),
            ("Cargar / Consultar", self.cargar_producto_en_formulario, "Secundario.TButton", "search.png"),
            ("Actualizar", self.actualizar_producto, "Accion.TButton", "edit.png"),
            ("Eliminar", self.eliminar_producto, "Eliminar.TButton", "delete.png"),
            ("Limpiar", self.limpiar_formulario_producto, "Secundario.TButton", "clean.png"),
        )

        for texto, comando, estilo, icono in botones:
            self.crear_boton_con_icono(acciones, texto, comando, estilo, icono).pack(
                fill="x", pady=(0, 7)
            )

        listado = self.crear_panel_listado(cuerpo, "Platos disponibles", usar_grid=True)
        self.tabla_productos = self.crear_tabla(
            listado,
            ("codigo", "nombre", "precio", "categoria", "tipo", "stock"),
            ("Codigo", "Nombre", "Precio", "Categoria", "Tipo", "Stock"),
            anchos=(55, 130, 70, 100, 110, 55),
        )
        self.refrescar_productos()

    def obtener_datos_producto(self):
        assert self.producto_codigo_entry is not None
        assert self.producto_nombre_entry is not None
        assert self.producto_precio_entry is not None
        assert self.producto_categoria_combo is not None
        assert self.producto_vegetariano_var is not None
        assert self.producto_stock_spin is not None

        return (
            self.producto_codigo_entry.get(),
            self.producto_nombre_entry.get(),
            self.producto_precio_entry.get(),
            self.producto_categoria_combo.get(),
            self.producto_vegetariano_var.get(),
            self.producto_stock_spin.get(),
        )

    def registrar_producto(self):
        try:
            self.restaurante_servicio.registrar_producto(*self.obtener_datos_producto())
            self.limpiar_formulario_producto()
            self.refrescar_productos()
            messagebox.showinfo("Platos", "Plato registrado correctamente.")
        except ValueError as error:
            messagebox.showerror("Platos", str(error))

    def cargar_producto_en_formulario(self):
        assert self.producto_codigo_entry is not None

        producto = self.restaurante_servicio.buscar_producto_por_codigo(
            self.producto_codigo_entry.get()
        )
        if producto is None:
            messagebox.showerror("Platos", "No existe un plato con ese codigo.")
            return

        self.limpiar_formulario_producto()
        self.producto_codigo_entry.insert(0, producto.codigo)
        self.producto_nombre_entry.insert(0, producto.nombre)
        self.producto_precio_entry.insert(0, f"{producto.precio:.2f}")
        self.producto_categoria_combo.set(producto.categoria)
        self.producto_vegetariano_var.set(producto.es_vegetariano)
        self.producto_stock_spin.insert(0, str(producto.stock))

    def actualizar_producto(self):
        try:
            self.restaurante_servicio.actualizar_producto(*self.obtener_datos_producto())
            self.refrescar_productos()
            messagebox.showinfo("Platos", "Plato actualizado correctamente.")
        except ValueError as error:
            messagebox.showerror("Platos", str(error))

    def eliminar_producto(self):
        assert self.producto_codigo_entry is not None

        try:
            self.restaurante_servicio.eliminar_producto(self.producto_codigo_entry.get())
            self.limpiar_formulario_producto()
            self.refrescar_productos()
            messagebox.showinfo("Platos", "Plato eliminado correctamente.")
        except ValueError as error:
            messagebox.showerror("Platos", str(error))

    def limpiar_formulario_producto(self):
        for entrada in (
            self.producto_codigo_entry,
            self.producto_nombre_entry,
            self.producto_precio_entry,
            self.producto_stock_spin,
        ):
            assert entrada is not None
            entrada.delete(0, tk.END)

        assert self.producto_categoria_combo is not None
        assert self.producto_vegetariano_var is not None
        self.producto_categoria_combo.set("")
        self.producto_vegetariano_var.set(False)
        self.producto_stock_spin.insert(0, "0")

    def refrescar_productos(self):
        assert self.tabla_productos is not None

        self.limpiar_tabla(self.tabla_productos)
        for producto in self.restaurante_servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                tk.END,
                values=(
                    producto.codigo,
                    producto.nombre,
                    f"${producto.precio:.2f}",
                    producto.categoria,
                    producto.etiqueta_tipo(),
                    producto.stock,
                ),
            )

        self.actualizar_barra_estado()

    def mostrar_funcionalidad_pendiente(self):
        messagebox.showinfo(
            "Proximamente",
            "Esta seccion se incorporara en una entrega posterior.",
        )

    # -------------------------------------------------------------------
    # Seccion Ventas: relaciona un cliente con un plato (Semana 15).
    # El boton usa command= para disparar el callback de venta, que
    # obtiene la seleccion de la interfaz y delega todo el registro,
    # la validacion y la persistencia a RestauranteServicio.
    # -------------------------------------------------------------------
    def mostrar_ventas(self):
        self.marcar_seccion("Ventas")
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Gestion de ventas")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(
            cuerpo,
            text="Registrar venta",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=14,
            pady=14,
        )
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        self.usuario_venta_combo = self.crear_campo_seleccion(
            formulario, "Cliente", 0, self.obtener_opciones_usuarios_venta()
        )
        self.producto_venta_combo = self.crear_campo_seleccion(
            formulario, "Plato", 1, self.obtener_opciones_productos_venta()
        )

        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        # command= asocia el boton con el callback registrar_venta.
        self.crear_boton_con_icono(
            acciones, "Registrar venta", self.registrar_venta, "Accion.TButton", "add.png"
        ).pack(fill="x")

        listado = self.crear_panel_listado(cuerpo, "Ventas registradas", usar_grid=True)
        self.tabla_ventas = self.crear_tabla(
            listado,
            ("identificador", "usuario", "producto", "fecha"),
            ("Venta", "Cliente", "Plato", "Fecha"),
            anchos=(50, 195, 170, 80),
        )
        self.refrescar_ventas()

    def crear_campo_seleccion(self, contenedor, etiqueta, fila, opciones):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        combo = ttk.Combobox(
            contenedor,
            width=28,
            font=("Arial", 10),
            state="readonly",
            values=list(opciones.keys()),
        )
        combo.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return combo

    def obtener_opciones_usuarios_venta(self):
        # Relaciona cada texto visible del combo con la identificacion real del cliente.
        self.opciones_usuarios_venta = {
            f"{usuario.identificacion} - {usuario.nombre}": usuario.identificacion
            for usuario in self.restaurante_servicio.listar_usuarios()
        }
        return self.opciones_usuarios_venta

    def obtener_opciones_productos_venta(self):
        # Relaciona cada texto visible del combo con el codigo real del plato.
        self.opciones_productos_venta = {
            f"{producto.codigo} - {producto.nombre}": producto.codigo
            for producto in self.restaurante_servicio.listar_productos()
        }
        return self.opciones_productos_venta

    def registrar_venta(self):
        assert self.usuario_venta_combo is not None
        assert self.producto_venta_combo is not None

        usuario_identificacion = self.opciones_usuarios_venta.get(
            self.usuario_venta_combo.get(), ""
        )
        producto_codigo = self.opciones_productos_venta.get(
            self.producto_venta_combo.get(), ""
        )

        try:
            # El callback solo recolecta la seleccion; RestauranteServicio
            # valida al cliente y al plato, y persiste la venta.
            self.restaurante_servicio.registrar_venta(usuario_identificacion, producto_codigo)
            self.limpiar_formulario_venta()
            self.refrescar_ventas()
            messagebox.showinfo("Ventas", "Venta registrada correctamente.")
        except ValueError as error:
            messagebox.showerror("Ventas", str(error))

    def limpiar_formulario_venta(self):
        assert self.usuario_venta_combo is not None
        assert self.producto_venta_combo is not None

        self.usuario_venta_combo.set("")
        self.producto_venta_combo.set("")

    def refrescar_ventas(self):
        assert self.tabla_ventas is not None

        self.limpiar_tabla(self.tabla_ventas)
        for venta in self.restaurante_servicio.listar_ventas():
            usuario = self.restaurante_servicio.buscar_usuario_por_identificacion(
                venta.usuario_identificacion
            )
            producto = self.restaurante_servicio.buscar_producto_por_codigo(
                venta.producto_codigo
            )
            texto_usuario = (
                venta.usuario_identificacion if usuario is None else f"{usuario.identificacion} - {usuario.nombre}"
            )
            texto_producto = (
                venta.producto_codigo if producto is None else f"{producto.codigo} - {producto.nombre}"
            )
            self.tabla_ventas.insert(
                "",
                tk.END,
                values=(venta.identificador, texto_usuario, texto_producto, venta.fecha),
            )

        # Actualiza la barra de estado para reflejar de inmediato la nueva venta.
        self.actualizar_barra_estado()

    # -------------------------------------------------------------------
    # Utilidades de interfaz compartidas por las secciones.
    # -------------------------------------------------------------------
    def crear_titulo_seccion(self, texto):
        assert self.contenido is not None

        tk.Label(
            self.contenido,
            text=texto,
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 17, "bold"),
        ).pack(anchor="w", pady=(0, 14))

    def crear_campo(self, contenedor, etiqueta, fila):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        entrada = tk.Entry(contenedor, width=24, font=("Arial", 10))
        entrada.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return entrada

    def crear_campo_categoria(self, contenedor, etiqueta, fila):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        combo = ttk.Combobox(
            contenedor,
            width=21,
            font=("Arial", 10),
            state="readonly",
            values=Producto.CATEGORIAS_VALIDAS,
        )
        combo.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return combo

    def crear_campo_vegetariano(self, contenedor, fila):
        variable = tk.BooleanVar(value=False)
        check = ttk.Checkbutton(
            contenedor,
            text="Es vegetariano",
            variable=variable,
            style="Vegetariano.TCheckbutton",
        )
        check.grid(row=fila, column=0, columnspan=2, sticky="w", pady=(0, 8))
        return variable

    def crear_campo_stock(self, contenedor, etiqueta, fila):
        tk.Label(
            contenedor,
            text=etiqueta,
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        spin = ttk.Spinbox(contenedor, from_=0, to=999, width=22, font=("Arial", 10))
        spin.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        spin.delete(0, tk.END)
        spin.insert(0, "0")
        return spin

    def crear_panel_listado(self, contenedor, titulo, usar_grid=False):
        listado = tk.LabelFrame(
            contenedor,
            text=titulo,
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=12,
            pady=12,
        )

        if usar_grid:
            listado.grid(row=0, column=1, sticky="nsew")
        else:
            listado.pack(fill="both", expand=True)

        return listado

    def crear_tabla(self, contenedor, columnas, encabezados, anchos=None):
        frame_tabla = tk.Frame(contenedor, bg=self.color_panel)
        frame_tabla.pack(fill="both", expand=True)

        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
        barra = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra.set)

        anchos = anchos or [120] * len(columnas)
        for columna, encabezado, ancho in zip(columnas, encabezados, anchos):
            tabla.heading(columna, text=encabezado)
            tabla.column(columna, width=ancho, anchor="w")

        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tabla

    def limpiar_tabla(self, tabla):
        for item in tabla.get_children():
            tabla.delete(item)

    def cerrar_sesion(self):
        self.al_cerrar_sesion()
