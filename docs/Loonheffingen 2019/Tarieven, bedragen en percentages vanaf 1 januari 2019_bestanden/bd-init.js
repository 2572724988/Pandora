function getURL(a) {
  a.dir = location.href.substring(0, location.href.lastIndexOf("/")), a.dom = a.dir, "http://" == a.dom.substr(0, 7) && (a.dom = a.dom.substr(7)), a.path = "";
  var b = a.dom.indexOf("/");
  b > -1 && (a.path = a.dom.substr(b + 1), a.dom = a.dom.substr(0, b)), a.port = "";
  var b = a.dom.indexOf(":");
  return b > -1 && (a.port = a.dom.substr(b + 1)), a.page = location.href.substring(a.dir.length + 1, location.href.length + 1), b = a.page.indexOf("?"), b > -1 && (a.page = a.page.substring(0, b)), b = a.page.indexOf("#"), b > -1 && (a.page = a.page.substring(0, b)), a.ext = "", b = a.page.indexOf("."), b > -1 && (a.ext = a.page.substring(b + 1), a.page = a.page.substr(0, b)), a.file = a.page, "" != a.ext && (a.file += "." + a.ext), "" == a.file && (a.page = "index"), "" == a.path ? a.pathdocroot = "/" + a.file : a.pathdocroot = "/" + a.path + "/" + a.file, a.args = [], -1 != location.href.indexOf("?") && (-1 != location.href.indexOf("&") ? a.args = location.href.substr(location.href.indexOf("?") + 1).split("&") : a.args[0] = location.href.substr(location.href.indexOf("?") + 1)), a.bookmark = location.hash, -1 != a.bookmark.indexOf("?") && (a.bookmark = a.bookmark.substr(0, a.bookmark.indexOf("?"))), a
}

function initActions_ckAccepted() {
  var a = new Array;
  return a
}

function Actions_ckAccepted(a) {
  for (var b = 0; b < a.length; b++) $(a[b][0]).html(a[b][1])
}

function CookiesAccepted() {
  AcceptCookies = !0;
}

function checkCKTO() {
  if ("undefined" != typeof ckto && "" != ckto) {
    var a = document.createElement("script");
    a.setAttribute("type", "text/javascript"), a.setAttribute("src", ckto), document.getElementsByTagName("head")[0].appendChild(a)
  }
}

var uri = new Object, _paq = _paq || [];
_paq.push(["setCookieDomain", "*.belastingdienst.nl", "*.belastingdienst.local"]), _paq.push(["setDomains", ["*.belastingdienst.nl", "*.douane.nl", "*.fiod.nl", "*.toeslagen.nl"]]), _paq.push(["trackPageView"]), _paq.push(["enableLinkTracking"]), function () {
  var a = "//pwa001.belastingdienst.nl/piwik/";
  _paq.push(["setTrackerUrl", a + "piwik.php"]), _paq.push(["setSiteId", 3]);
  var b = document, c = b.createElement("script"), d = b.getElementsByTagName("script")[0];
  c.type = "text/javascript", c.async = !0, c.defer = !0, c.src = a + "piwik.js", d.parentNode.insertBefore(c, d)
}(), $(document).ready(function () {
  $("#bd-nojs").remove(), uri = getURL(uri),  CookiesAccepted()
});

var RO = RO || {};
!function (a, b) {
  String.prototype.hashCode = function () {
    var a, b, c = 0, d = this.length;
    if (0 == d) return c;
    for (a = 0; d > a; a++) b = this.charCodeAt(a), c = (c << 5) - c + b, c &= c;
    return c
  }, ("undefined" == typeof b.console || "undefined" == typeof b.console.log) && (b.console = {
    log: function () {
    }
  }), RO.cookies = {
    supported: !1, domain: "", init: function () {
      var a, c, d, e, f, g, h = this, i = b.location.hostname.split("."), j = i.length;
      for (a in this) "function" != typeof this[a] && (this[a] = void 0);
      if (h.domain = "local" === i[j - 1] || "nl" === i[j - 1] ? "." + i[j - 2] + "." + i[j - 1] : "." + i[j - 1], h.test()) for (g = document.cookie.split("; "), a = 0, c = g.length; c > a; a++) d = g[a].indexOf("="), -1 !== d && (e = g[a].substr(0, d), f = g[a].substr(d + 1, g[a].length), h[e] = f)
    }, test: function () {
      var a = this;
      return a.create("deeg", "waar", 1), null !== a.read("deeg") && (a.supported = !0, a.erase("deeg")), a
    }, create: function (a, b, c) {
      var d, e, f = this, g = "";
      c && (d = new Date, d.setTime(d.getTime() + 24 * c * 60 * 60 * 1e3), g = "; expires=" + d.toGMTString()), e = "" !== f.domain ? "; domain=" + f.domain : "", document.cookie = a + "=" + b + g + "; path=/" + e + ";secure", this[a] = b
    }, read: function (a) {
      for (var b, c = a + "=", d = document.cookie.split(";"), e = 0, f = d.length; f > e; e++) {
        for (b = d[e]; " " === b.charAt(0);) b = b.substring(1, b.length);
        if (0 === b.indexOf(c)) return b.substring(c.length, b.length)
      }
      return null
    }, erase: function (a) {
      this.create(a, "", -1), this[a] = void 0
    }, eraseAll: function () {
      for (var a in this) "function" != typeof this[a] && this.erase(a)
    }
  }
}(document, window), $(document).ready(function () {
  RO.cookies.init();
});
