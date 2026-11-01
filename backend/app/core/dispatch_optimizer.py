import math
from typing import List, Dict, Any, Tuple
from ..utils.geo_utils import haversine_distance_meters

class DispatchRouteOptimizer:
    """
    Field Crew Dispatch Optimizer (A10).
    Solves priority-weighted routing with 2-opt local search and compares against FIFO baseline.
    """

    def __init__(self, avg_speed_kmh: float = 25.0, service_time_mins: float = 30.0):
        self.avg_speed_kmh = avg_speed_kmh
        self.service_time_mins = service_time_mins

    def _route_distance_km(self, start_pos: Tuple[float, float], tickets: List[Dict[str, Any]]) -> float:
        if not tickets:
            return 0.0
        total_m = 0.0
        curr_lat, curr_lon = start_pos
        for t in tickets:
            t_lat = t.get("lat", curr_lat)
            t_lon = t.get("lon", curr_lon)
            total_m += haversine_distance_meters(curr_lat, curr_lon, t_lat, t_lon)
            curr_lat, curr_lon = t_lat, t_lon
        return round(total_m / 1000.0, 2)

    def optimize_route(
        self,
        crew_location: Tuple[float, float],
        tickets: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Produce optimized route sequence with 2-opt refinement and compare against FIFO baseline.
        """
        if not tickets:
            return {
                "optimized_sequence": [],
                "fifo_sequence": [],
                "optimized_distance_km": 0.0,
                "fifo_distance_km": 0.0,
                "km_saved": 0.0,
                "pct_distance_reduction": 0.0,
                "fuel_saved_liters": 0.0
            }

        fifo_tickets = list(tickets)
        fifo_distance = self._route_distance_km(crew_location, fifo_tickets)

        # 1. Greedy Priority-Weighted Nearest Insertion
        unvisited = list(tickets)
        optimized = []
        curr_lat, curr_lon = crew_location

        while unvisited:
            best_idx = 0
            best_score = float("inf")

            for idx, candidate in enumerate(unvisited):
                c_lat = candidate.get("lat", curr_lat)
                c_lon = candidate.get("lon", curr_lon)
                dist_km = haversine_distance_meters(curr_lat, curr_lon, c_lat, c_lon) / 1000.0
                
                # Priority factor: higher priority lowers the cost
                urgency = candidate.get("urgency", "Medium")
                urgency_weight = 0.5 if urgency == "Critical" else (0.8 if urgency == "High" else 1.0)
                sla_rem = max(1.0, float(candidate.get("sla_hours_remaining", 24)))
                sla_urgency_factor = min(2.0, 24.0 / sla_rem)

                cost = (dist_km * urgency_weight) / (1.0 + 0.3 * (sla_urgency_factor - 1.0))
                if cost < best_score:
                    best_score = cost
                    best_idx = idx

            chosen = unvisited.pop(best_idx)
            optimized.append(chosen)
            curr_lat = chosen.get("lat", curr_lat)
            curr_lon = chosen.get("lon", curr_lon)

        # 2. 2-Opt Local Search Improvement
        improved = True
        iterations = 0
        best_opt_dist = self._route_distance_km(crew_location, optimized)

        while improved and iterations < 50:
            improved = False
            iterations += 1
            for i in range(len(optimized) - 1):
                for j in range(i + 1, len(optimized)):
                    # Reverse segment [i:j+1]
                    new_route = optimized[:i] + optimized[i:j+1][::-1] + optimized[j+1:]
                    new_dist = self._route_distance_km(crew_location, new_route)
                    if new_dist < best_opt_dist - 0.01:
                        optimized = new_route
                        best_opt_dist = new_dist
                        improved = True
                        break
                if improved:
                    break

        optimized_distance = self._route_distance_km(crew_location, optimized)
        km_saved = max(0.0, round(fifo_distance - optimized_distance, 2))
        pct_reduction = round((km_saved / fifo_distance * 100.0), 1) if fifo_distance > 0 else 0.0
        # Average utility squad vehicle fuel consumption ~ 8 km/L
        fuel_saved_liters = round(km_saved / 8.0, 2)

        return {
            "optimized_sequence": [t.get("master_ticket_id") for t in optimized],
            "fifo_sequence": [t.get("master_ticket_id") for t in fifo_tickets],
            "optimized_distance_km": optimized_distance,
            "fifo_distance_km": fifo_distance,
            "km_saved": km_saved,
            "pct_distance_reduction": pct_reduction,
            "fuel_saved_liters": fuel_saved_liters,
            "tasks_count": len(tickets)
        }

dispatch_optimizer = DispatchRouteOptimizer()
