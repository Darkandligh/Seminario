Prompt que le di a la IA para el borrador de pruebas:

Escribe pruebas con pytest para estas funciones de A-Fénix. No modifiques el código.
Usa @pytest.mark.parametrize con un comentario por fila, pytest.approx para decimales,
pytest.raises con el tipo de error exacto y esperados fijos que salgan de la regla.

1. cambiar_estado(comanda, nuevo, rol, ahora=None) -> Comanda, en afenix/estados.py.
   Lanza SinPermiso y CambioInvalido.
   Regla (HU-06 y HU-07): la comanda pasa de recibido a en preparación y de en
   preparación a listo, un paso a la vez; no puede saltar ni retroceder. Cuando queda
   lista se guarda la hora de entrega. Solo la cocina cambia el estado.
2. minutos_espera(hora_entrada, ahora) -> float, en afenix/cocina.py. Lanza ValueError.
   Regla (HU-05): la pantalla de cocina muestra cuánto lleva esperando cada comanda,
   contado desde su hora de entrada.
3. comandas_para_cocina(comandas) -> list[Comanda], en afenix/cocina.py.
   Regla (HU-04): la cocina ve las comandas en orden de llegada, por hora de entrada.

Las comandas se crean con registrar_comanda(mesa, items, ahora) de afenix/comandas.py.
