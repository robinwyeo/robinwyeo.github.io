/**
 * avilist-phylo-loader.js
 *
 * Lazy-loads the Phylocanvas.gl CDN bundle once per page and exposes a
 * helper ``window.renderAvilistPhyloTree(containerId, options)`` for use
 * by the AviList page embeds.
 *
 * The embeds inserted by ``nbconvert_avilist_postprocess.py`` call their own
 * inline IIFE, which already handles CDN loading.  This file provides a
 * named, re-usable entry point for manual or future use.
 */

(function (global) {
  "use strict";

  var CDN_URL =
    "https://unpkg.com/@phylocanvas/phylocanvas.gl@1/dist/bundle.min.js";

  /**
   * Ensure Phylocanvas.gl is loaded, then call cb().
   * @param {function} cb  Called when window.phylocanvas is ready.
   */
  function _ensureLoaded(cb) {
    if (global.phylocanvas && global.phylocanvas.PhylocanvasGL) {
      cb();
      return;
    }
    var tag = document.querySelector('script[data-phylocanvas-loader="true"]');
    if (!tag) {
      tag = document.createElement("script");
      tag.src = CDN_URL;
      tag.setAttribute("data-phylocanvas-loader", "true");
      document.head.appendChild(tag);
    }
    tag.addEventListener("load", cb, { once: true });
  }

  /**
   * Render a Phylocanvas.gl tree into the given container.
   *
   * @param {string} containerId  ID of the <div> to render into.
   * @param {Object} opts
   * @param {string} opts.newick      Newick tree string (required).
   * @param {Object} opts.meta        Tip-metadata dict {tipName: {color, label}}.
   * @param {string} [opts.treeType]  "circular" | "radial" | "rectangular".
   * @param {number} [opts.height]    Canvas height in pixels (default 700).
   * @returns {void}
   */
  function renderAvilistPhyloTree(containerId, opts) {
    opts = opts || {};

    _ensureLoaded(function () {
      var container = document.getElementById(containerId);
      if (!container) {
        console.warn("[avilist-phylo-loader] container not found:", containerId);
        return;
      }

      var treeTypes = global.phylocanvas.TreeTypes;
      var typeMap = {
        circular:     treeTypes.Circular,
        radial:       treeTypes.Radial,
        rectangular:  treeTypes.Rectangular,
        hierarchical: treeTypes.Hierarchical,
      };

      var height = opts.height || 700;
      var meta   = opts.meta   || {};

      // Build per-tip styles
      var styles = {};
      Object.keys(meta).forEach(function (tip) {
        var m = meta[tip];
        styles[tip] = {
          fillColour:   m.color || "#aaaaaa",
          strokeColour: m.color || "#aaaaaa",
          shape:        "circle",
          size:         5,
          label:        m.label || tip,
        };
      });

      var tree = new global.phylocanvas.PhylocanvasGL(container, {
        size:               { width: container.clientWidth, height: height },
        source:             opts.newick || "",
        type:               typeMap[opts.treeType || "circular"] || treeTypes.Circular,
        showLabels:         true,
        alignLabels:        true,
        showInternalLabels: false,
        showBranchLengths:  false,
        interactive:        true,
        styles:             styles,
      });

      global.addEventListener("resize", function () {
        tree.setProps({ size: { width: container.clientWidth, height: height } });
      });
    });
  }

  // Expose on window
  global.renderAvilistPhyloTree = renderAvilistPhyloTree;

}(window));
