class Graphier:
    import pandas as pd

    def __init__(
        self, 
        data: pd.DataFrame, 
        target: str = None):
        
        import networkx as nx

        self.target = target
        self.data = data

        if self.target:
            self.feature = [target] + [x for x in self.data.columns if x != self.target]
        else:
            self.feature = [x for x in self.data.columns]

        self._nodes = [x for x in range(len(self.feature))]
        self._label = {idx: col for idx, col in enumerate(self.feature)}
        self._inverted_label = {v: k for k, v in self._label.items()}
        self._node_pairs = []
        self.Graph = nx.Graph()

    def _compute_correlation(
            self, 
            method: str = "pearson", 
            corr_threshold: float = 0.15
    ):

        from itertools import combinations

        feature_pairs = list(combinations(self.feature, 2))

        if method == "kendall":
            from scipy.stats import kendalltau as corr
        elif method == "spearman":
            from scipy.stats import spearmanr as corr
        elif method == "pearson":
            from scipy.stats import pearsonr as corr
        else:
            raise Exception(
                "parameter 'method' should be in ['kendall', 'spearman', 'pearson']"
            )

        for feat1, feat2 in feature_pairs:
            _correlation = corr(self.data[feat1], self.data[feat2])
            if abs(_correlation[0]) > corr_threshold and _correlation[1] < 0.05:
                self._node_pairs.append(
                    (
                        self._inverted_label[feat1],
                        self._inverted_label[feat2],
                        round(_correlation[0], 3),
                    )
                )
            else:
                continue

        if len(self._node_pairs) == 0:
            raise Exception("No Correlation Pairs :: Decrease corr_threshold")
        else:
            return self

    def build_graph(self, statistics, method: str, corr_threshold: float = 0.15):

        if statistics == "correlation":
            self._compute_correlation(method=method, corr_threshold=corr_threshold)

        self.Graph.add_nodes_from(self._label.keys())
        self.Graph.add_weighted_edges_from(self._node_pairs)

        return self, self.Graph

    def draw_graph(
            self,
            path_to_save: str = None,
            figsize=(20, 20),
            node_size: float = 1,
            font_size: float = 1,
            edge_width=10,
            show_coef: bool = False,
            coef_font_size: float = 1,
            label_pos_coef: float = 0.5,
    ):
        
        import networkx as nx
        import matplotlib.pyplot as plt
        import numpy as np

        if self.target:
            pos = nx.circular_layout(self.Graph, scale=100)
            pos[self._inverted_label[self.target]] = np.array([0.5, 0.5])
        else:
            pos = nx.spiral_layout(self.Graph, scale=100, equidistant=True)

        positive_edges, positive_weights = zip(
            *[
                (edge, d)
                for edge, d in nx.get_edge_attributes(self.Graph, "weight").items()
                if d > 0
            ]
        )
        
        negative_edges, negative_weights = zip(
            *[
                (edge, d)
                for edge, d in nx.get_edge_attributes(self.Graph, "weight").items()
                if d < 0
            ]
        )

        positive_width = tuple([edge_width * w for w in positive_weights])
        negative_width = tuple([edge_width * w for w in positive_weights])

        positive_edge_labels = {
            edge: d
            for edge, d in nx.get_edge_attributes(self.Graph, "weight").items()
            if d > 0
        }
        negative_edge_labels = {
            edge: d
            for edge, d in nx.get_edge_attributes(self.Graph, "weight").items()
            if d < 0
        }

        node_degree = dict(nx.degree(self.Graph))

        node_color = "teal"
        edgecolors = "white"

        plt.rcParams["axes.facecolor"] = "black"
        plt.rcParams["savefig.facecolor"] = "black"
        plt.rcParams["axes.edgecolor"] = "white"

        fig = plt.figure("Graph", figsize=figsize, facecolor="black")

        axgrid = fig.add_gridspec(5, 4)

        ax0 = fig.add_subplot(axgrid[0:3, :])
        ax0.set_title("All Relationships", fontsize=font_size * 18, color="white")

        nx.draw_networkx_nodes(
            G=self.Graph,
            pos=pos,
            node_color=node_color,
            edgecolors=edgecolors,
            node_size=[(v + 1) * 100 * node_size for v in node_degree.values()],
            alpha=1,
            ax=ax0,
        )
        nx.draw_networkx_edges(
            self.Graph,
            pos,
            edgelist=positive_edges,
            width=positive_width,
            alpha=0.95,
            edge_vmin=0,
            edge_vmax=1,
            edge_color=positive_weights,
            edge_cmap=plt.cm.Reds,
            ax=ax0,
        )

        nx.draw_networkx_edges(
            self.Graph,
            pos,
            edgelist=negative_edges,
            width=negative_width,
            alpha=0.95,
            edge_vmin=-1,
            edge_vmax=0,
            edge_color=negative_weights,
            edge_cmap=plt.cm.Blues_r,
            ax=ax0,
        )

        nx.draw_networkx_labels(
            self.Graph,
            pos,
            labels=self._label,
            font_color="white",
            font_size=font_size * 10,
            bbox=dict(
                facecolor="white",
                alpha=0,
                edgecolor="black",
                boxstyle="round,pad=0.3",
            ),
            ax=ax0,
        )

        ax1 = fig.add_subplot(axgrid[3:, :2])
        ax1.set_title("Positive Relationships", fontsize=font_size * 10, color="white")

        nx.draw_networkx_nodes(
            G=self.Graph,
            pos=pos,
            node_color=node_color,
            edgecolors=edgecolors,
            node_size=[(v + 1) * 70 * node_size for v in node_degree.values()],
            alpha=1,
            ax=ax1,
        )
        nx.draw_networkx_edges(
            self.Graph,
            pos,
            edgelist=positive_edges,
            width=positive_width,
            alpha=0.95,
            edge_vmin=0,
            edge_vmax=1,
            edge_color=positive_weights,
            edge_cmap=plt.cm.Reds,
            ax=ax1,
        )
        nx.draw_networkx_labels(
            self.Graph,
            pos,
            labels=self._label,
            font_color="white",
            font_size=font_size * 13,
            bbox=dict(
                facecolor="white",
                alpha=0,
                edgecolor="black",
                boxstyle="round,pad=0.3",
            ),
            ax=ax1,
        )

        ax2 = fig.add_subplot(axgrid[3:, 2:])
        ax2.set_title("Negative Relationships", fontsize=font_size * 10, color="white")

        nx.draw_networkx_nodes(
            G=self.Graph,
            pos=pos,
            node_color=node_color,
            edgecolors=edgecolors,
            node_size=[(v + 1) * 70 * node_size for v in node_degree.values()],
            alpha=1,
            ax=ax2,
        )
        nx.draw_networkx_edges(
            self.Graph,
            pos,
            edgelist=negative_edges,
            width=negative_width,
            alpha=0.95,
            edge_vmin=-1,
            edge_vmax=0,
            edge_color=negative_weights,
            edge_cmap=plt.cm.Blues_r,
            ax=ax2,
        )
        nx.draw_networkx_labels(
            self.Graph,
            pos,
            labels=self._label,
            font_color="white",
            font_size=font_size * 12,
            bbox=dict(
                facecolor="white",
                alpha=0,
                edgecolor="black",
                boxstyle="round,pad=0.3",
            ),
            ax=ax2,
        )

        if show_coef:
            nx.draw_networkx_edge_labels(
                self.Graph,
                pos,
                positive_edge_labels,
                font_size=coef_font_size * 14,
                font_color="indianred",
                bbox=dict(facecolor="white", alpha=1, edgecolor="black"),
                label_pos=label_pos_coef,
                verticalalignment="baseline",
                ax=ax0,
            )
            nx.draw_networkx_edge_labels(
                self.Graph,
                pos,
                negative_edge_labels,
                font_size=coef_font_size * 14,
                font_color="royalblue",
                bbox=dict(facecolor="white", alpha=1, edgecolor="black"),
                label_pos=label_pos_coef,
                verticalalignment="baseline",
                ax=ax0,
            )

            nx.draw_networkx_edge_labels(
                self.Graph,
                pos,
                positive_edge_labels,
                font_size=coef_font_size * 13,
                font_color="indianred",
                bbox=dict(facecolor="white", alpha=1, edgecolor="black"),
                label_pos=label_pos_coef,
                verticalalignment="baseline",
                ax=ax1,
            )

            nx.draw_networkx_edge_labels(
                self.Graph,
                pos,
                negative_edge_labels,
                font_size=coef_font_size * 12,
                font_color="royalblue",
                bbox=dict(facecolor="white", alpha=1, edgecolor="black"),
                label_pos=label_pos_coef,
                verticalalignment="baseline",
                ax=ax2,
            )

        plt.tight_layout()

        if path_to_save:
            plt.savefig(path_to_save)

        plt.show()
