class RouteOptimizer:
    def select_best_route(self, loss_results):
        """
        loss_results: list of dicts
        Each dict must contain:
            - route_id
            - total_loss
        """

        if not loss_results:
            return None

        best = min(loss_results, key=lambda r: r["total_loss"])
        return best
