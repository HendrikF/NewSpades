from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from Vector import *
from Texture import *
from Collision import *

class Renderer(object):
    def __init__(self, ns):
        self.ns = ns
        self.farplane = 50
        self.background = [0.5, 0.9, 1, 1]
    
    def start(self):
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        
        glEnable(GL_CULL_FACE)
        glCullFace(GL_FRONT)
        
        glEnable(GL_FOG)
        glFogfv(GL_FOG_COLOR, self.background)
        #glFogf(GL_FOG_MODE, GL_LINEAR)
        #glFogf(GL_FOG_START, 10)
        #glFogf(GL_FOG_END, 25)
        glFogf(GL_FOG_DENSITY, 0.015)
        
        #glEnable(GL_LIGHTING)
        #glEnable(GL_COLOR_MATERIAL)
        #glEnable(GL_LIGHT0)
        #glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
        #glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
        #glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
        #glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 10.0, 0.0))
        
        self.textures = {
            "5": Texture("img")
        }
        
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glLineWidth(2)
    
    def reset(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(self.background[0], self.background[1], self.background[2], self.background[3])
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluPerspective(45, self.ns.ratio, 0.1, self.farplane)
        
        position = self.ns.player.getEyePosition()
        lookat = position + self.ns.player.getWorldVector(Vector(1, 0, 0))
        up = self.ns.player.getWorldVector(Vector(0, 0, 1))
        gluLookAt(
            position[0],
            position[1],
            position[2],
            lookat[0],
            lookat[1],
            lookat[2],
            up[0],
            up[1],
            up[2]
        )
    
    def render(self):
        self.reset()
        
        self.renderMap()
        
        self.renderLookAt()
        
        # Test Overlay
        """
        self.textures["5"].enable()
        
        tl = self.ns.player.getEyePosition() + self.ns.player.getWorldVector(Vector(0.2,  0.08,  0.08))
        tr = self.ns.player.getEyePosition() + self.ns.player.getWorldVector(Vector(0.2, -0.08,  0.08))
        bl = self.ns.player.getEyePosition() + self.ns.player.getWorldVector(Vector(0.2,  0.08, -0.08))
        br = self.ns.player.getEyePosition() + self.ns.player.getWorldVector(Vector(0.2, -0.08, -0.08))
        
        glEnable(GL_BLEND)
        
        glBegin(GL_QUADS)
        
        glTexCoord2f(0, 0)
        glVertex3f(bl[0], bl[1], bl[2])
        
        glTexCoord2f(0, 1)
        glVertex3f(tl[0], tl[1], tl[2])
        
        glTexCoord2f(1, 1)
        glVertex3f(tr[0], tr[1], tr[2])
        
        glTexCoord2f(1, 0)
        glVertex3f(br[0], br[1], br[2])
        
        glEnd()
        
        glDisable(GL_BLEND)
        """
    
    def renderLookAt(self):
        block = Collision.lookAtBlock(self.ns.player, self.ns.map)
        if block != False:
            glDisable(GL_CULL_FACE)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            faces = self.ns.map.getAllBlockFaces(block[1].x, block[1].y, block[1].z)
            glColor3f(0, 0, 0)
            for face in faces:
                self.renderQuadrat(face[0], face[1], face[2], face[3])
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glEnable(GL_CULL_FACE)
    
    def renderMap(self):
        #self.textures["5"].enable()
        for face, color in self.ns.map.getFaces():
            glColor3f(color[0], color[1], color[2])
            self.renderQuadrat(face[0], face[1], face[2], face[3])
    
    def renderQuadrat(self, p1, p2, p3, p4):
        glBegin(GL_QUADS)
        
        #glTexCoord2f(0, 0)
        glVertex3f(p1[0], p1[1], p1[2])
        
        #glTexCoord2f(0, 1)
        glVertex3f(p2[0], p2[1], p2[2])
        
        #glTexCoord2f(1, 1)
        glVertex3f(p3[0], p3[1], p3[2])
        
        #glTexCoord2f(1, 0)
        glVertex3f(p4[0], p4[1], p4[2])
        
        glEnd()
