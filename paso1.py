# -*- encoding: utf-8 -*-
#
# Creamos las escenas y el menú del juego

import pilasengine

pilas = pilasengine.iniciar()

class Escena_Juego(pilasengine.escenas.Escena):
    """ Escena principal del juego. """

    def iniciar(self):
        # Cargamos el fondo del juego.
        self.imagen = pilas.fondos.Pasto()


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

pilas.escenas.Escena_Menu()


pilas.ejecutar()
