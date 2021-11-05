import math


class Trigonometry:
    @staticmethod
    def sin(alpha) -> float:
        return math.sin(
            math.radians(
                alpha
            )
        )
    
    @staticmethod
    def tan(alpha) -> float:
        return math.tan(
            math.radians(
                alpha
            )
        )

    @staticmethod
    def cos(alpha) -> float:
        return math.cos(
            math.radians(
                alpha
            )
        )
