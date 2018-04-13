# -*- encoding: utf-8 -*-

import random
import pilasengine

pilas = pilasengine.iniciar()
pilas.reiniciar_si_cambia(__file__)

teclas2 = {
            pilas.simbolos.a: 'izquierda',
            pilas.simbolos.d: 'derecha',
            pilas.simbolos.w: 'arriba',
            pilas.simbolos.s: 'abajo',
            pilas.simbolos.CTRL: 'boton',
        }

class Municion1(pilasengine.actores.Actor):

	def iniciar(self):
		self.imagen=pilas.imagenes.cargar_grilla("disparo.png", 2)

class Municion2(pilasengine.actores.Actor):

	def iniciar(self):
		self.imagen=pilas.imagenes.cargar_grilla("disparo.png", 2)

class Tanque1(pilasengine.actores.Actor):

    def iniciar(self):
        self.aprender("LimitadoABordesDePantalla")
        self.aprender("PuedeExplotar")
        #x = random.randrange(-320, 320)
        y = random.randrange(-240, 160)
        #self.x = x
        self.y = y

        self.imagen = "images/tanque.png"
        self.rotacion = 90
        self.aprender("MoverseComoCoche", velocidad_maxima=2, deceleracion=0.05, velocidad_rotacion=0.5)
        self.aprender("Disparar", frecuencia_de_disparo=2, angulo_salida_disparo=90, municion='Municion1')

    def aumentar_velocidad(self):
		self.aprender("MoverseComoCoche", velocidad_maxima=8, deceleracion=0.05, velocidad_rotacion=0.5)

    def reducir_velocidad(self):
		self.aprender("MoverseComoCoche", velocidad_maxima=2, deceleracion=0.05, velocidad_rotacion=0.5)

    def actualizar(self):
        pass


class Tanque2(pilasengine.actores.Actor):

	def iniciar(self):

		self.mi_control = pilas.control.Control(teclas2)
		self.aprender("LimitadoABordesDePantalla")
		self.aprender("PuedeExplotar")
		self.y = random.randrange(-240, 160)
		self.imagen = "images/tanque2.png"
		self.rotacion = 270
		self.aprender("MoverseComoCoche", control=self.mi_control, velocidad_maxima=2, deceleracion=0.05, velocidad_rotacion=0.5)
		self.aprender("Disparar", control=self.mi_control, frecuencia_de_disparo=2, angulo_salida_disparo=90, municion='Municion2')

	def aumentar_velocidad(self):
		self.aprender("MoverseComoCoche", control= self.mi_control, velocidad_maxima=8, deceleracion=0.05, velocidad_rotacion=0.5)

	def reducir_velocidad(self):
		self.aprender("MoverseComoCoche", control= self.mi_control, velocidad_maxima=2, deceleracion=0.05, velocidad_rotacion=0.5)

	def actualizar(self):
		pass



class Escena_Juego(pilasengine.escenas.Escena):
    """ Escena principal del juego. """

    def iniciar(self):
        # Cargamos el fondo del juego.
        self.imagen = pilas.fondos.Pasto()

        tanque1= pilas.actores.Tanque1()
        self.tanque1 = tanque1
        tanque1.x = 200

        texto_t1 = pilas.actores.Texto("Rojo:", x=-250, y=200)
        texto_t1.definir_color(pilas.colores.blanco)
        vidas1 = pilas.actores.Puntaje(x=-210, y=200)
        vidas1.aumentar("3")
        self.vidas1 = vidas1

        tanque2 = pilas.actores.Tanque2()
        self.tanque2 = tanque2
        tanque2.x = -200

        texto_t2 = pilas.actores.Texto("Verde:", x=210, y=200)
        texto_t2.definir_color(pilas.colores.blanco)
        vidas2 = pilas.actores.Puntaje(x=260, y=200)
        vidas2.aumentar("3")
        self.vidas2 = vidas2

        pilas.colisiones.agregar("Municion1", "Tanque2", self.impacto1)
        pilas.colisiones.agregar("Municion2", "Tanque1", self.impacto2)


        ###colisiones entre tanques y estrellas cambiadas aquí###
        pilas.colisiones.agregar("Tanque1", "Estrella", self._aumentar_velocidad)
        pilas.colisiones.agregar("Tanque2", "Estrella", self._aumentar_velocidad)

        self.tarea_estrella = pilas.tareas.siempre(3, self.crear_estrella)




    def crear_tanque1(self):

        tanque1= pilas.actores.Tanque1()
        tanque1.x = 200

    def crear_tanque2(self):

        tanque2 = pilas.actores.Tanque2()
        tanque2.x = -200

    def impacto1(self, proyectil1, enemigo1):
        proyectil1.eliminar()
        pilas.actores.Humo(proyectil1.x, proyectil1.y)
        enemigo1.eliminar()

        self.vidas1.reducir()

        if self.vidas1.obtener() > 0:
            #self.vidas1.reducir()
            self.crear_tanque2()
        elif self.vidas1.obtener() == 0:
            self.tarea_estrella.terminar()# terminamos la tarea crear estrellas
            self.efecto_ganador(self.tanque1)
            #self.tanque2.eliminar()

    def impacto2(self, proyectil2, enemigo2):
        proyectil2.eliminar()
        pilas.actores.Humo(proyectil2.x, proyectil2.y)
        enemigo2.eliminar()

        self.vidas2.reducir()

        if self.vidas2.obtener() > 0:
            #self.vidas2.reducir()
            self.crear_tanque1()
        elif self.vidas2.obtener() == 0:
            self.efecto_ganador(self.tanque2)
            #self.tanque1.eliminar()

    def efecto_ganador(self, ganador):

        ganador.x = [0]
        ganador.y = [0]
        ganador.escala = [3]
        ganador.rotacion = [360]

    def crear_estrella(self):
        x = random.randrange(-320, 320)
        y = random.randrange(-240, 240)
        estrella = pilas.actores.Estrella(x, y)
        estrella.escala = 0.4

    def _aumentar_velocidad(self, tanque, estrella):
        tanque.aumentar_velocidad()
        #tanque.aprender("MoverseComoCoche", velocidad_maxima=4)
        pilas.tareas.agregar(5, tanque.reducir_velocidad)
        estrella.eliminar()

    def actualizar(self):
        pass

class Escena_Menu(pilasengine.escenas.Escena):
    """ Escena del menú del juego. """

    def iniciar(self):
        # Cargamos el fondo del juego.
        pilas.fondos.Tarde()
        menu = pilas.actores.Menu(
        [
        (u'Iniciar Juego', self.iniciar_juego),
        (u'Salir', self.salir_del_juego),
        ]
        )

    def salir_del_juego(self):
        pilas.terminar()

    def iniciar_juego(self):
        pilas.escenas.Escena_Juego()


pilas.escenas.vincular(Escena_Menu)
pilas.escenas.vincular(Escena_Juego)

pilas.actores.vincular(Municion1)
pilas.actores.vincular(Municion2)
pilas.actores.vincular(Tanque1)
pilas.actores.vincular(Tanque2)

pilas.escenas.Escena_Menu()


pilas.ejecutar()
