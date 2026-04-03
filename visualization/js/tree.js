const SUBSET_SIZE = 5;

/**
 * WordTree class for D3.js tree visualization with collapsible nodes
 */
class WordTree {
    constructor(containerId, width = 1400, height = 900) {
        this.containerId = containerId;
        this.width = width;
        this.height = height;
        this.margin = { top: 40, right: 120, bottom: 20, left: 120 };
        this.duration = 750; // Animation duration in ms
        this.nodeRadius = 5;
        this.colorMode = 'era';

        // Zoom constraints
        this.minZoom = 0.1;  // Can zoom out to 10% of original size
        this.maxZoom = 3;    // Can zoom in to 300% of original size

        // Create SVG
        this.svg = d3.select(containerId)
            .attr('width', this.width)
            .attr('height', this.height);

        // Create container group for zoom/pan
        this.zoomContainer = this.svg.append('g');

        // Create tree group inside zoom container
        this.g = this.zoomContainer.append('g')
            .attr('transform', `translate(${this.margin.left},${this.height / 2})`);

        // Initialize zoom behavior
        this.zoom = d3.zoom()
            .scaleExtent([this.minZoom, this.maxZoom])
            .on('zoom', (event) => this.handleZoom(event));

        // Apply zoom to SVG
        this.svg.call(this.zoom);

        // Create tree layout
        this.treemap = d3.tree()
            .nodeSize([30, 180]); // [vertical px per node, horizontal px per level]

        this.root = null;
        this.i = 0; // Node ID counter
    }

    /**
     * Load and render tree data
     * @param {Object} treeData - Hierarchical tree data
     */
    loadData(treeData) {
        // Clear existing tree
        this.g.selectAll('*').remove();
        this.i = 0;

        // Create hierarchy
        this.root = d3.hierarchy(treeData, d => d.children);
        this.root.x0 = this.height / 2;
        this.root.y0 = 0;

        // Save full sorted children list for pagination
        this.allRootChildren = this.root.children ? [...this.root.children] : [];

        // Reset zoom to default view
        this.resetZoom();
    }

    /**
     * Collapse a node's children recursively
     * @param {Object} d - Node to collapse
     */
    collapse(d) {
        if (d.children) {
            const realChildren = d.children.filter(c => !c.data._isSentinel);
            if (!d._allChildren) d._allChildren = realChildren;
            d._children = d._allChildren;
            d._children.forEach(child => this.collapse(child));
            d.children = null;
        }
    }

    /**
     * Expand a node's children
     * @param {Object} d - Node to expand
     */
    expand(d) {
        if (d._children) {
            d.children = d._children;
            d._children = null;
        }
    }

    /**
     * Display a page of root children
     * @param {number} page - 1-based page number
     * @param {number} pageSize - Number of children per page
     */
    setPage(page, pageSize) {
        const start = (page - 1) * pageSize;
        this.root.children = this.allRootChildren.slice(start, start + pageSize);
        this.root.children.forEach(child => this.collapse(child));
        this.update(this.root);
    }

    get totalRootChildren() {
        return this.allRootChildren ? this.allRootChildren.length : 0;
    }

    createSentinel(parent, showMore) {
        const all = parent._allChildren;
        const count = parent._visibleCount;
        const name = showMore
            ? `\u25bc ${Math.min(SUBSET_SIZE, all.length - count)} more`
            : `\u25b2 ${Math.min(SUBSET_SIZE, count - SUBSET_SIZE)} less`;
        return {
            data: { name, _isSentinel: true, _showMore: showMore },
            depth: parent.depth + 1,
            height: 0,
            parent: parent,
            children: null,
            _children: null,
            id: `sentinel-${showMore ? 'more' : 'less'}-${parent.id}`,
            x: 0, x0: 0, y: 0, y0: 0
        };
    }

    renderChildren(d) {
        const slice = d._allChildren.slice(0, d._visibleCount);
        const sentinels = [];
        if (d._visibleCount < d._allChildren.length) sentinels.push(this.createSentinel(d, true));
        if (d._visibleCount > SUBSET_SIZE) sentinels.push(this.createSentinel(d, false));
        d.children = [...slice, ...sentinels];
    }

    expandToSubset(d) {
        d._visibleCount = Math.min(SUBSET_SIZE, d._allChildren.length);
        this.renderChildren(d);
        d._children = null;
    }

    /**
     * Toggle children on click
     * @param {Event} event - Click event
     * @param {Object} d - Node data
     */
    click(event, d) {
        if (d.data._isSentinel) {
            const parent = d.parent;
            const total = parent._allChildren.length;
            if (d.data._showMore) {
                parent._visibleCount = Math.min(parent._visibleCount + SUBSET_SIZE, total);
            } else {
                parent._visibleCount = Math.max(parent._visibleCount - SUBSET_SIZE, SUBSET_SIZE);
            }
            this.renderChildren(parent);
            this.update(parent);
            return;
        }

        if (d.children) {
            d._children = d._allChildren;
            d.children = null;
        } else {
            if (!d._allChildren) d._allChildren = d._children;
            this.expandToSubset(d);
        }
        this.update(d);
    }

    /**
     * Update tree visualization with transitions
     * @param {Object} source - Source node for the update
     */
    update(source) {
        const self = this;

        // Compute new tree layout
        const treeData = this.treemap(this.root);
        const nodes = treeData.descendants();
        const links = treeData.descendants().slice(1);

        // Normalize for fixed-depth
        nodes.forEach(d => { d.y = d.depth * 180; });

        // ===== Update nodes =====
        const node = this.g.selectAll('g.node')
            .data(nodes, d => d.id || (d.id = ++this.i));

        // Enter new nodes at parent's previous position
        const nodeEnter = node.enter().append('g')
            .attr('class', d => d.data._isSentinel ? 'node sentinel' : 'node')
            .attr('transform', d => `translate(${source.y0},${source.x0})`)
            .on('click', (event, d) => this.click(event, d));

        nodeEnter.append('circle')
            .attr('r', 1e-6)
            .style('fill', d => {
                if (d.data._isSentinel) return '#ccc';
                return d._children ? 'lightsteelblue' : '#fff';
            });

        nodeEnter.append('text')
            .attr('dy', '.35em')
            .attr('x', d => d.children || d._children ? -13 : 13)
            .attr('text-anchor', d => d.children || d._children ? 'end' : 'start')
            .text(d => d.data._isSentinel
                ? d.data.name
                : `${d.data.name} (${formatNumber(d.data.value || 0)})`)
            .style('fill-opacity', 1e-6);

        // Transition nodes to their new position
        const nodeUpdate = nodeEnter.merge(node);

        nodeUpdate.transition()
            .duration(this.duration)
            .attr('transform', d => `translate(${d.y},${d.x})`);

        nodeUpdate.select('circle')
            .attr('r', this.nodeRadius)
            .style('fill', d => {
                if (d.data._isSentinel) return '#ccc';
                if (d._children) return 'lightsteelblue';
                return getNodeColor(d, this.colorMode);
            })
            .attr('cursor', 'pointer');

        nodeUpdate.select('text')
            .style('fill-opacity', 1);

        // Remove exiting nodes
        const nodeExit = node.exit().transition()
            .duration(this.duration)
            .attr('transform', d => `translate(${source.y},${source.x})`)
            .remove();

        nodeExit.select('circle')
            .attr('r', 1e-6);

        nodeExit.select('text')
            .style('fill-opacity', 1e-6);

        // ===== Update links =====
        const link = this.g.selectAll('path.link')
            .data(links, d => d.id);

        const linkEnter = link.enter().insert('path', 'g')
            .attr('class', 'link')
            .attr('d', d => {
                const o = { x: source.x0, y: source.y0 };
                return this.diagonal(o, o);
            });

        const linkUpdate = linkEnter.merge(link);

        linkUpdate.transition()
            .duration(this.duration)
            .attr('d', d => this.diagonal(d, d.parent));

        link.exit().transition()
            .duration(this.duration)
            .attr('d', d => {
                const o = { x: source.x, y: source.y };
                return this.diagonal(o, o);
            })
            .remove();

        // Store old positions for transition
        nodes.forEach(d => {
            d.x0 = d.x;
            d.y0 = d.y;
        });
    }

    /**
     * Create curved links between nodes
     * @param {Object} s - Source node position
     * @param {Object} d - Destination node position
     * @returns {string} - SVG path string
     */
    diagonal(s, d) {
        return `M ${s.y} ${s.x}
                C ${(s.y + d.y) / 2} ${s.x},
                  ${(s.y + d.y) / 2} ${d.x},
                  ${d.y} ${d.x}`;
    }

    /**
     * Expand all nodes recursively
     */
    expandAll() {
        const expandRecursive = (d) => {
            if (d._children) {
                d.children = d._children;
                d._children = null;
            }
            if (d.children) {
                d.children.forEach(expandRecursive);
            }
        };

        if (this.root) {
            expandRecursive(this.root);
            this.update(this.root);
        }
    }

    /**
     * Collapse all nodes to first level
     */
    collapseAll() {
        if (this.root && this.root.children) {
            this.root.children.forEach(child => this.collapse(child));
            this.update(this.root);
        }
    }

    /**
     * Set color mode and refresh visualization
     * @param {string} mode - Either 'era' or 'speaker'
     */
    setColorMode(mode) {
        this.colorMode = mode;
        if (this.root) {
            this.update(this.root);
        }
    }

    /**
     * Highlight nodes matching search term
     * @param {string} searchTerm - Term to search for
     * @returns {number} - Number of matching nodes
     */
    highlightNodes(searchTerm) {
        // Clear previous highlights
        this.g.selectAll('g.node').classed('highlighted', false);

        if (!searchTerm || !this.root) return 0;

        // Find matching nodes
        const results = searchTree(this.root, searchTerm);

        // Highlight them
        results.forEach(node => {
            const nodeSelection = this.g.selectAll('g.node')
                .filter(d => d === node);
            nodeSelection.classed('highlighted', true);
        });

        return results.length;
    }

    /**
     * Handle zoom/pan events
     * @param {Object} event - D3 zoom event
     */
    handleZoom(event) {
        this.zoomContainer.attr('transform', event.transform);
    }

    /**
     * Reset zoom to initial view
     */
    resetZoom() {
        this.svg.transition()
            .duration(750)
            .call(
                this.zoom.transform,
                d3.zoomIdentity
            );
    }

    /**
     * Zoom to fit all visible nodes
     */
    zoomToFit() {
        if (!this.root) return;

        // Get bounds of all nodes
        const nodes = this.root.descendants();
        if (nodes.length === 0) return;

        let minX = Infinity, maxX = -Infinity;
        let minY = Infinity, maxY = -Infinity;

        nodes.forEach(d => {
            if (d.x !== undefined && d.y !== undefined) {
                minX = Math.min(minX, d.x);
                maxX = Math.max(maxX, d.x);
                minY = Math.min(minY, d.y);
                maxY = Math.max(maxY, d.y);
            }
        });

        // Add padding
        const padding = 50;
        const dx = maxX - minX + padding * 2;
        const dy = maxY - minY + padding * 2;

        // Calculate scale to fit
        const scale = Math.min(
            this.width / dy,
            this.height / dx,
            this.maxZoom
        );

        // Calculate translation to center
        const translate = [
            this.width / 2 - scale * (minY + dy / 2),
            this.height / 2 - scale * (minX + dx / 2)
        ];

        // Apply transform with transition
        this.svg.transition()
            .duration(750)
            .call(
                this.zoom.transform,
                d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale)
            );
    }
}
