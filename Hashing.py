def fnv1_32(data: bytes) -> int:
	"""Calcula el hash FNV-1 de 32 bits para los bytes proporcionados.

	Especificación FNV-1 (32-bit):
	  offset_basis = 2166136261
	  FNV_prime = 16777619

	Args:
		data: bytes a hashear.

	Returns:
		Entero sin signo de 32 bits con el hash.
	"""
	fnv_prime = 16777619
	offset_basis = 2166136261
	h = offset_basis
	for byte in data:
		h = (h * fnv_prime) & 0xFFFFFFFF
		h = h ^ byte
	return h


def format_hash_32(h: int) -> str:
	return f"0x{h:08x}"


def main() -> None:
	try:
		mensaje = input("Ingrese el mensaje: ")
	except EOFError:
		mensaje = ""

	b = mensaje.encode("utf-8")
	h = fnv1_32(b)

	print()
	print("Resumen (hash) del mensaje usando FNV-1 (32-bit):")
	print(f"  Mensaje: {mensaje}")
	print(f"  Hash (hex): {format_hash_32(h)}")
	print(f"  Hash (decimal): {h}")


if __name__ == "__main__":
	main()
