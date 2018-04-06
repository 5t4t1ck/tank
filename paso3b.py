# -*- encoding: utf-8 -*-
#
# Creamos las escenas y el menú del juego

import random
import pilasengine

pilas = pilasengine.iniciar()
pilas.reiniciar_si_cambia(__file__)

teclas2 = {
            pilas.simbolos.a: 'izquierda',
            pilas.simbolos.d: 'derecha',
            pilas.simbolos.w: 'arriba',
            pilas.simbolos.s: 'abajo',
            pilas.simbolos.ALTGR: 'boton',
        }

class Tanque(pilasengine.actores.Actor):

    def iniciar(self):
        self.aprender("LimitadoABordesDePantalla")
        self.aprender("PuedeExplotar")

    def actualizar(self):
        pass

    def definir_enemigo(self, enemigo):
        self.aprender("Disparar", frecuencia_de_disparo=2, angulo_salida_disparo=90)
        self.enemigo = enemigo

    def impacto(self, proyectil, enemigo):
        proyectil.eliminar()
        pilas.actores.Humo(proyectil.x, proyectil.y)

class Escena_Juego(pilasengine.escenas.Escena):
    """ Escena principal del juego. """

    def iniciar(self):
        # Cargamos el fondo del juego.
        self.imagen = pilas.fondos.Pasto()

        tanque1= pilas.actores.Tanque()
        tanque1.x = 200
        tanque1.imagen = "images/tanque.png"
        tanque1.rotacion = 90
        mi_control = pilas.control.Control(teclas2)
        tanque1.aprender("MoverseComoCoche", control=mi_control,velocidad_maxima=2, deceleracion=0.05, velocidad_rotacion=0.5)

        tanque1.aprender("Disparar", frecuencia_de_disparo=2, angulo_salida_disparo=90)
        tanque1_vidas = pilas.actores.Puntaje(x=250, y=200, color="blanco")

        tanque2 = pilas.actores.Tanque()
        tanque2.x = -200
        tanque2.imagen = "images/tanque2.png"
        tanque1.rotacion = 90
        tanque2.aprender("MoverseComoCoche", velocidad_maxima=2, deceleracion=0.05, velocidad_rotacion=0.5)
        #tanque2.aprender("Disparar", frecuencia_de_disparo=2, angulo_salida_disparo=90)
        tanque2_vidas = pilas.actores.Puntaje(x=-250, y=200, color="blanco")

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

pilas.actores.vincular(Tanque)

pilas.escenas.Escena_Menu()


pilas.ejecutar()
