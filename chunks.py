import ctypes

import pyglet.gl as gl

CHUNK_WIDTH = 16
CHUNK_HEIGHT = 16
CHUNK_LENGHT = 16

class Chunk:
    def __init__(self, chunk_position):
        self.chunk_position = chunk_position

        self.position = (
            self.chunk_position[0] * CHUNK_WIDTH,
            self.chunk_position[1] * CHUNK_HEIGHT,
            self.chunk_position[2] * CHUNK_LENGHT)
        
        self.has_mesh = False

        self.mesh_vertex_positions = []
        self.mesh_tex_cords = []
        self.mesh_shading_values = []

        self.mesh_index_counter = 0
        self.mesh_indices = []

        self.vao = gl.GLuint(0)
        gl.glGenVertexArrays(1, self.vao)
        gl.glBindVertexArray(self.vao)

        self.vertex_position_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, self.vertex_position_vbo)

        self.tex_cord_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, self.tex_cord_vbo)

        self.shading_values_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, self.shading_values_vbo)

        self.ibo = gl.GLuint(0)
        gl.glGenBuffers(1, self.ibo)


    def update_mesh(self, block_type):
        self.has_mesh = True
        self.mesh_vertex_positions = []
        self.mesh_tex_cords = []
        self.mesh_shading_values = []

        self.mesh_index_counter = 0
        self.mesh_indices = []

        for local_x in range(CHUNK_WIDTH):
            for local_y in range(CHUNK_HEIGHT):
                for local_z in range(CHUNK_LENGHT):
                    x, y, z = (
                        self.position[0] + local_x,
                        self.position[1] + local_y,
                        self.position[2] + local_z)
                    
                    vertex_positions = block_type.vertex_positions.copy()

                    for i in range(24):
                        vertex_positions[i * 3 + 0] += x
                        vertex_positions[i * 3 + 1] += y
                        vertex_positions[i * 3 + 2] += z
                    
                    self.mesh_vertex_positions.extend(vertex_positions)

                    indices = block_type.indices.copy()
                    for i in range(36):
                        indices[i] += self.mesh_index_counter

                    self.mesh_indices.extend(indices)
                    self.mesh_index_counter += 24

                    self.mesh_tex_cords.extend(block_type.tex_coords)
                    self.mesh_shading_values.extend(block_type.shading_values)

        if not self.mesh_index_counter:
            return

        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_position_vbo)
        gl.glBufferData(
			gl.GL_ARRAY_BUFFER,
			ctypes.sizeof(gl.GLfloat * len(self.mesh_vertex_positions)),
			(gl.GLfloat * len(self.mesh_vertex_positions)) (*self.mesh_vertex_positions),
			gl.GL_STATIC_DRAW)
                
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(0)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.tex_cord_vbo)
        gl.glBufferData(
			gl.GL_ARRAY_BUFFER,
			ctypes.sizeof(gl.GLfloat * len(self.mesh_tex_cords)),
			(gl.GLfloat * len(self.mesh_tex_cords)) (*self.mesh_tex_cords),
			gl.GL_STATIC_DRAW)
                
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.shading_values_vbo)
        gl.glBufferData(
			gl.GL_ARRAY_BUFFER,
			ctypes.sizeof(gl.GLfloat * len(self.mesh_shading_values)),
			(gl.GLfloat * len(self.mesh_shading_values)) (*self.mesh_shading_values),
			gl.GL_STATIC_DRAW)
                
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(2)


        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.ibo)
        gl.glBufferData(
			gl.GL_ARRAY_BUFFER,
			ctypes.sizeof(gl.GLfloat * len(self.mesh_indices)),
			(gl.GLfloat * len(self.mesh_indices)) (*self.mesh_indices),
			gl.GL_STATIC_DRAW)
        
    def draw(self):
        if not self.mesh_index_counter:
            return
        gl.glDrawElements(
			gl.GL_TRIANGLES,
			len(self.mesh_indices),
			gl.GL_UNSIGNED_INT,
			None)
