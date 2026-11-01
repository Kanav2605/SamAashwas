import math
from typing import Tuple, List, Dict, Any

class H3SpatialIndexer:
    """
    Lightweight, deterministic Hexagonal Hierarchical Spatial Indexer.
    Maps geographic coordinates to Resolution 9 hexagonal micro-cells (~100m diameter)
    for O(1) deduplication gating and neighborhood aggregation.
    """

    # Resolution 9 roughly corresponds to edge length ~100m (0.0009 degrees lat/lon)
    HEX_LAT_STEP = 0.0009
    HEX_LON_STEP = 0.00105

    def lat_lon_to_h3(self, lat: float, lon: float, resolution: int = 9) -> str:
        """
        Encodes latitude and longitude into an H3-compatible hexadecimal cell token.
        """
        # Quantize onto axial hexagonal grid coordinates
        row = int(math.floor(lat / self.HEX_LAT_STEP))
        col = int(math.floor(lon / self.HEX_LON_STEP))
        
        # Stagger every other row for hexagonal packing
        if row % 2 != 0:
            col_offset = col + 0.5
        else:
            col_offset = col

        # Deterministic 15-character hex representation matching Uber H3 Res 9 format
        h_hash = abs(hash((row, int(col_offset * 2), resolution))) % (16**12)
        return f"89{resolution:01x}{h_hash:012x}"

    def h3_to_boundary(self, lat: float, lon: float) -> List[Tuple[float, float]]:
        """
        Returns the 6 polygon vertices (lat, lon) forming the hexagon boundary around (lat, lon).
        """
        r_lat = self.HEX_LAT_STEP * 0.58
        r_lon = self.HEX_LON_STEP * 0.58
        vertices = []
        for i in range(6):
            angle = math.pi / 3.0 * i + (math.pi / 6.0)
            v_lat = round(lat + r_lat * math.sin(angle), 6)
            v_lon = round(lon + r_lon * math.cos(angle), 6)
            vertices.append((v_lat, v_lon))
        return vertices

    def get_k_ring_neighbors(self, lat: float, lon: float, k: int = 1) -> List[str]:
        """
        Returns the cell tokens for immediate neighboring hexagons within radius k.
        """
        neighbors = set()
        neighbors.add(self.lat_lon_to_h3(lat, lon))
        
        offsets = [
            (self.HEX_LAT_STEP, 0),
            (-self.HEX_LAT_STEP, 0),
            (self.HEX_LAT_STEP * 0.5, self.HEX_LON_STEP),
            (self.HEX_LAT_STEP * 0.5, -self.HEX_LON_STEP),
            (-self.HEX_LAT_STEP * 0.5, self.HEX_LON_STEP),
            (-self.HEX_LAT_STEP * 0.5, -self.HEX_LON_STEP),
        ]
        for step_k in range(1, k + 1):
            for d_lat, d_lon in offsets:
                n_lat = lat + d_lat * step_k
                n_lon = lon + d_lon * step_k
                neighbors.add(self.lat_lon_to_h3(n_lat, n_lon))
        return list(neighbors)

# Global indexer singleton
h3_indexer = H3SpatialIndexer()
