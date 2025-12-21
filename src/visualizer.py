"""
ForkMonkey Visualizer - Cat Edition
"""

import math
from typing import Dict, List
from src.genetics import MonkeyDNA, TraitCategory, Rarity

class MonkeyVisualizer:
    """Generates generic SVG cat art from DNA"""

    BODY_COLORS = {
        "brown": {"main": "#8B4513", "shadow": "#5D2E0C", "highlight": "#A0522D"},
        "tan": {"main": "#D2B48C", "shadow": "#B8956E", "highlight": "#E8D4B8"},
        "beige": {"main": "#F5F5DC", "shadow": "#D4D4B8", "highlight": "#FFFFF0"},
        "gray": {"main": "#808080", "shadow": "#5A5A5A", "highlight": "#A0A0A0"},
        "golden": {"main": "#FFD700", "shadow": "#B8860B", "highlight": "#FFEC8B"},
        "silver": {"main": "#C0C0C0", "shadow": "#909090", "highlight": "#E8E8E8"},
        "white": {"main": "#FFFFFF", "shadow": "#E0E0E0", "highlight": "#FFFFFF"},
        "black": {"main": "#333333", "shadow": "#000000", "highlight": "#555555"},
        "orange": {"main": "#FFA500", "shadow": "#CC8400", "highlight": "#FFB732"},
    }

    BACKGROUNDS = {
        "white": {"type": "solid", "color": "#F8F9FA"},
        "blue_sky": {"type": "gradient", "id": "sky-gradient"},
        "green_grass": {"type": "gradient", "id": "grass-gradient"},
        "sunset": {"type": "gradient", "id": "sunset-gradient"},
        "space": {"type": "scene", "base": "#0D1B2A", "elements": "stars"},
    }

    @classmethod
    def generate_svg(cls, dna: MonkeyDNA, width: int = 400, height: int = 400) -> str:
        traits = {
            "body_color": dna.traits[TraitCategory.BODY_COLOR].value,
            "expression": dna.traits[TraitCategory.FACE_EXPRESSION].value,
            "accessory": dna.traits[TraitCategory.ACCESSORY].value,
            "pattern": dna.traits[TraitCategory.PATTERN].value,
            "background": dna.traits[TraitCategory.BACKGROUND].value,
            "special": dna.traits[TraitCategory.SPECIAL].value,
        }
        seed = int(dna.dna_hash[:8], 16) if dna.dna_hash else 12345

        svg_parts = [
            f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
            cls._generate_defs(),
            cls._generate_background(traits["background"], width, height, seed),
            cls._generate_body(traits["body_color"], traits["pattern"], width, height, seed),
            cls._generate_face(traits["expression"], width, height),
            "</svg>",
        ]
        return "\n".join(svg_parts)

    @classmethod
    def _generate_defs(cls) -> str:
        return '''<defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="2" dy="4" stdDeviation="3" flood-opacity="0.3"/>
    </filter>
    <linearGradient id="sky-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#87CEEB"/><stop offset="100%" stop-color="#E0F4FF"/>
    </linearGradient>
</defs>'''

    @classmethod
    def _generate_background(cls, bg: str, w: int, h: int, seed: int) -> str:
         # Placeholder simple background
        return f'<rect width="{w}" height="{h}" fill="#F0F8FF"/>'

    @classmethod
    def _generate_body(cls, color: str, pattern: str, w: int, h: int, seed: int) -> str:
        cx, cy = w // 2, h // 2
        c = cls.BODY_COLORS.get(color, cls.BODY_COLORS["gray"])
        parts = []

        # Ears (Pointy for cat)
        parts.append(f'<polygon points="{cx-60},{cy-80} {cx-90},{cy-140} {cx-30},{cy-100}" fill="{c["main"]}" filter="url(#shadow)"/>')
        parts.append(f'<polygon points="{cx+60},{cy-80} {cx+90},{cy-140} {cx+30},{cy-100}" fill="{c["main"]}" filter="url(#shadow)"/>')
        
        # Inner Ears
        parts.append(f'<polygon points="{cx-60},{cy-85} {cx-80},{cy-125} {cx-40},{cy-100}" fill="#FFB6C1"/>')
        parts.append(f'<polygon points="{cx+60},{cy-85} {cx+80},{cy-125} {cx+40},{cy-100}" fill="#FFB6C1"/>')

        # Head
        parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="100" ry="90" fill="{c["main"]}" filter="url(#shadow)"/>')
        
        # Whiskers
        for y in [10, 20, 30]:
            parts.append(f'<line x1="{cx-40}" y1="{cy+y}" x2="{cx-120}" y2="{cy+y-10}" stroke="#000" stroke-width="2" opacity="0.5"/>')
            parts.append(f'<line x1="{cx+40}" y1="{cy+y}" x2="{cx+120}" y2="{cy+y-10}" stroke="#000" stroke-width="2" opacity="0.5"/>')

        return "\n".join(parts)

    @classmethod
    def _generate_face(cls, expr: str, w: int, h: int) -> str:
        cx, cy = w // 2, h // 2
        parts = []
        
        # Eyes (Slit pupils for cat)
        parts.append(f'<ellipse cx="{cx-35}" cy="{cy-15}" rx="20" ry="25" fill="#FFF"/>')
        parts.append(f'<ellipse cx="{cx+35}" cy="{cy-15}" rx="20" ry="25" fill="#FFF"/>')
        parts.append(f'<ellipse cx="{cx-35}" cy="{cy-15}" rx="5" ry="18" fill="#000"/>')
        parts.append(f'<ellipse cx="{cx+35}" cy="{cy-15}" rx="5" ry="18" fill="#000"/>')
        
        # Cute nose
        parts.append(f'<polygon points="{cx-10},{cy+25} {cx+10},{cy+25} {cx},{cy+35}" fill="#FFB6C1"/>')
        
        # Mouth
        parts.append(f'<path d="M{cx-10} {cy+35} Q{cx-15} {cy+45} {cx-25} {cy+40}" stroke="#000" stroke-width="2" fill="none"/>')
        parts.append(f'<path d="M{cx+10} {cy+35} Q{cx+15} {cy+45} {cx+25} {cy+40}" stroke="#000" stroke-width="2" fill="none"/>')
        
        return "\n".join(parts)

    @classmethod
    def generate_thumbnail(cls, dna: MonkeyDNA, size: int = 100) -> str:
        return cls.generate_svg(dna, width=size, height=size)

def main():
    pass

if __name__ == "__main__":
    main()
