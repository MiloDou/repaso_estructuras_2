import heapq
import collections
from typing import Dict, Optional, Tuple


class Node:
	def __init__(self, freq: int, char: Optional[str] = None, left: 'Node' = None, right: 'Node' = None):
		self.freq = freq
		self.char = char
		self.left = left
		self.right = right

	def __lt__(self, other: 'Node') -> bool:
		return self.freq < other.freq


def build_huffman_tree(freqs: Dict[str, int]) -> Optional[Node]:
	heap = [Node(freq, char) for char, freq in freqs.items()]
	if not heap:
		return None
	heapq.heapify(heap)

	
	if len(heap) == 1:
		only = heapq.heappop(heap)
		return Node(only.freq, None, left=only)

	while len(heap) > 1:
		a = heapq.heappop(heap)
		b = heapq.heappop(heap)
		merged = Node(a.freq + b.freq, None, left=a, right=b)
		heapq.heappush(heap, merged)

	return heapq.heappop(heap)


def build_codes(node: Optional[Node], prefix: str, codes: Dict[str, str]) -> None:
	if node is None:
		return
	if node.char is not None:
		codes[node.char] = prefix or '0'
		return
	build_codes(node.left, prefix + '0', codes)
	build_codes(node.right, prefix + '1', codes)


def compress_message(message: str) -> Tuple[str, Dict[str, str]]:
	freqs = collections.Counter(message)
	root = build_huffman_tree(freqs)
	codes: Dict[str, str] = {}
	build_codes(root, '', codes)

	compressed_bits = ''.join(codes[ch] for ch in message)
	return compressed_bits, codes


def bits_to_size(bits_len: int) -> Tuple[int, int]:
	"""Devuelve (bits, bytes) dado el número de bits; bytes redondeados hacia arriba."""
	bytes_len = (bits_len + 7) // 8
	return bits_len, bytes_len


def main() -> None:
	try:
		mensaje = input('Ingrese el mensaje a comprimir: ')
	except EOFError:
		mensaje = ''

	original_bytes = len(mensaje.encode('utf-8'))
	original_bits = original_bytes * 8

	compressed_bits_str, codes = compress_message(mensaje)
	compressed_bits = len(compressed_bits_str)
	compressed_bytes = (compressed_bits + 7) // 8

	print()
	print('Compresión Huffman (sencilla)')
	print(f'  Mensaje: {mensaje}')
	print(f'  Tamaño original: {original_bits} bits ({original_bytes} bytes)')
	print(f'  Tamaño comprimido: {compressed_bits} bits ({compressed_bytes} bytes)')
	if original_bits > 0:
		ratio = compressed_bits / original_bits
		print(f'  Ratio comprimido: {ratio:.3f} (comprimido / original)')
		savings = (1 - ratio) * 100
		print(f'  Ahorro: {savings:.2f}%')
	else:
		print('  Ratio comprimido: N/A (mensaje vacío)')

	print('\n  Códigos usados:')
	for ch, code in sorted(codes.items(), key=lambda x: (len(x[1]), x[0])):
		display = ch if ch != '\n' else '\\n'
		print(f'    {repr(display)} : {code}')


	if compressed_bits > 0:
		muestra = compressed_bits_str[:128]
		if len(compressed_bits_str) > len(muestra):
			muestra += '...'
		print(f'\n  Primeros bits comprimidos (hasta 128): {muestra}')


if __name__ == '__main__':
	main()

