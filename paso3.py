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

    def actualizar(self):
        pass


class Tanque2(pilasengine.actores.Actor):

    def iniciar(self):
        self.aprender("LimitadoABordesDePantalla")
        self.aprender("PuedeExplotar")

    def actualizar(self):
        pass



class Escena_Juego(pilasengine.escenas.Escena):
    """ Escena principal del juego. """

    def iniciar(self):
        # Cargamos el fondo del juego.
        self.imagen = pilas.fondos.Pasto()

        tanque1= pilas.actores.Tanque1()
        tanque1.x = 200
        tanque1.imagen = "images/tanque.png"
        tanque1.rotacion = 90
        tanque1.aprender("MoverseComoCoche", velocidad_maxima=2, deceleracion=0.05, velocidad_rotacion=0.5)
        tanque1.aprender("Disparar", frecuencia_de_disparo=2, angulo_salida_disparo=90, municion='Municion1')
        tanque1_vidas = pilas.actores.Puntaje(x=250, y=200, color="blanco")

        mi_control = pilas.control.Control(teclas2)

        tanque2 = pilas.actores.Tanque2()
        tanque2.x = -200
        tanque2.imagen = "images/tanque2.png"
        tanque2.rotacion = 270
        tanque2.aprender("MoverseComoCoche", control=mi_control, velocidad_maxima=2, deceleracion=0.05, velocidad_rotacion=0.5)
        tanque2.aprender("Disparar", control=mi_control, frecuencia_de_disparo=2, angulo_salida_disparo=90, municion='Municion2')
        tanque2_vidas = pilas.actores.Puntaje(x=-250, y=200, color="blanco")

        pilas.colisiones.agregar("Municion1", "Tanque2", self.impacto)
        pilas.colisiones.agregar("Municion2", "Tanque1", self.impacto)

    def impacto(self, proyectil, enemigo):
        proyectil.eliminar()
        pilas.actores.Humo(proyectil.x, proyectil.y)
        #print("IMPACTO")
        enemigo.eliminar()

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
