import math
import random

import chunks

import block_type
import texture_manager

class World:
	def __init__(self):

		self.texture_manager = texture_manager.Texture_manager(16, 16, 256)
		self.block_types = [None]

		self.block_types.append(block_type.Block_type(self.texture_manager, "cobblestone", {"all": "cobblestone"}))
		self.block_types.append(block_type.Block_type(self.texture_manager, "grass", {"top": "grass", "bottom": "dirt", "sides": "grass_side"}))
		self.block_types.append(block_type.Block_type(self.texture_manager, "grass_block", {"all": "grass"}))
		self.block_types.append(block_type.Block_type(self.texture_manager, "dirt", {"all": "dirt"}))
		self.block_types.append(block_type.Block_type(self.texture_manager, "stone", {"all": "stone"}))
		self.block_types.append(block_type.Block_type(self.texture_manager, "sand", {"all": "sand"}))
		self.block_types.append(block_type.Block_type(self.texture_manager, "planks", {"all": "planks"}))
		self.block_types.append(block_type.Block_type(self.texture_manager, "log", {"top": "log_top", "bottom": "log_top", "sides": "log_side"}))

		self.texture_manager.generate_mipmaps()

		self.chunks = {}

		for x in range(8):
			for z in range(8):
				chunk_position = (x - 4, -1, z - 4)
				current_chunk = chunks.Chunk(self, chunk_position)
				
				for i in range(chunks.CHUNK_WIDTH):
					for j in range(chunks.CHUNK_HEIGHT):
						for k in range(chunks.CHUNK_LENGTH):
							if j > 13: current_chunk.blocks[i][j][k] = random.choice([0, 3])
							else: current_chunk.blocks[i][j][k] = random.choice([0, 0, 1])
				
				self.chunks[chunk_position] = current_chunk

		for chunk_position in self.chunks:
			self.chunks[chunk_position].update_mesh()
	
	def get_block_number(self, position):
		x, y, z = position
		
		chunk_position = (
			math.floor(x / chunks.CHUNK_WIDTH),
			math.floor(y / chunks.CHUNK_HEIGHT),
			math.floor(z / chunks.CHUNK_LENGTH))

		if not chunk_position in self.chunks:
			return 0

		local_x = int(x % chunks.CHUNK_WIDTH)
		local_y = int(y % chunks.CHUNK_HEIGHT)
		local_z = int(z % chunks.CHUNK_LENGTH)

		return self.chunks[chunk_position].blocks[local_x][local_y][local_z]
	
	def draw(self):
		for chunk_position in self.chunks:
			self.chunks[chunk_position].draw()