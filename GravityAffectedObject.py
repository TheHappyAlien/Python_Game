class GravityAffectedObject():
    def __init__(self, gravityScale, terminalVelocity = 1000000000) -> None:
        self.gravityScale = gravityScale
        self.yVelocity = 0
        self.terminalVelocity = terminalVelocity
        self.isGrounded = False

    def gravity(self) -> None:
        if not self.isGrounded and self.yVelocity <= self.terminalVelocity:
            self.yVelocity += self.gravityScale
        self.y += self.yVelocity