import chunks

import block_type
import texture_manager

class World:
    def __init__(self):
        self.texture_manager = texture_manager.Texture_manager(16 ,16, 256)
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
        self.chunks[(0, 0, 0)] = chunks.Chunk(self, (0, 0, 0))

        for x in range(chunks.CHUNK_WIDTH):
            for y in range(chunks.CHUNK_HEIGHT):
                for z in range(chunks.CHUNK_LENGTH):
                    self.chunks[(0, 0, 0)].blocks[x][y][z] = 1


    def draw(self):
        for chunk_position in self.chunks:
            self.chunks[chunk_position].draw()

