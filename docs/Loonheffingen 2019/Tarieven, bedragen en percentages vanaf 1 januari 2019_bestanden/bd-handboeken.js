
var bClientIsSafari = false;
var bClientIsIe = false;
var ua = navigator.userAgent.toLowerCase();

if (ua.indexOf('safari') !== -1 && ua.indexOf('chrome') === -1) {
    bClientIsSafari = true;
} else if (ua.indexOf('msie') !== -1) {
    bClientIsIe = true;
}
if (bClientIsIe){
    if(ua.indexOf('msie 7.0') !== -1 && window.location.href.indexOf('www-t') !== -1){
        if (loadUserData('msie7-warning',false)!=='getoond'){
            alert('Beste collega,' + "\n"
            + 'Navigeren in Internet Explorer 7.0 (modus) werkt minder prettig. ' + "\n"
            + 'Met F12 kunt u schakelen naar "Browser Mode 8".'
            );
            saveUserData('msie7-warning','getoond');
        }
    }

    if ("onhashchange" in window) {
        window.onhashchange = locationHashChanged;
    }

}

/*
 * locationHashChanged dient om ie met scrollable divs op te dragen, expleciet naar een id op pagina te navigeren.
 */
function locationHashChanged() {
    if (location.hash!==''){
        window.location.hash = location.hash;
    }else{
        $('#hoofd_content').animate({scrollTop: $('h1').offset().top}, 'fast');
    }
}

$('.fragmentIdentifier').click(function() {
    /*
     * Hier een oplossing voor een probleem met safari/internet explorer.
     * Zij vergeten het fragment/hash als er een redirect op de server plaats vindt.
     * Daarom bewaren we de hash in de 
     * localStorage -> Safari: Zie http://en.wikipedia.org/wiki/Web_storage
     * userData -> Internet Explorer: Zie http://msdn.microsoft.com/en-us/library/ms531424(v=vs.85).aspx
     */
    if (bClientIsSafari || bClientIsIe) {
        var hrefOrg = $(this).attr('href');
        if (hrefOrg.indexOf('#') !== 0) {
            if (bClientIsSafari) {
                event.preventDefault();
            } else {
                event.returnValue = false;
            }
            var hrefNew = hrefOrg.substring(0, hrefOrg.indexOf('#'));
            var hashToSave = hrefOrg.substring(hrefOrg.indexOf('#'));
            saveHash(hashToSave, bClientIsIe);
            $(location).attr('href', hrefNew);

        }
    }

});

$("a[href='#top']").click(function(e) {
    $('#hoofd_content').scrollTop(0);
});

$('.warningShowSource').click(function() {
    return confirm('Wil je echt de source in de browser bekijken?\nDit kan afhankelijk van de grootte en pc uren duren.\n\nOm de source te downloaden gebruik je de rechter muisknop en kies je "Opslaan als..."\n\nToch openen in Browser?\n');
});

if (bClientIsSafari || bClientIsIe) {
    var scrollToHash = loadHash(bClientIsIe);
    if (scrollToHash !== '') {
        window.location.hash = scrollToHash;
    }
}

/*
 * saveHash is een functie voor het opslaan van een hash.
 */
function saveHash(hashToSave, bClientIsIe) {
    var bdUserData = document.getElementById("bdUserData");
    if (typeof(Storage) !== "undefined") {
        window.localStorage.hash = hashToSave;
    }else{
        saveUserData('hash',hashToSave);
    }
}

/*
 * loadHash is een functie voor het opslaan van een hash.
 */
function loadHash(bClientIsIe) {
    var hashToLoad = '';
    if (typeof(Storage) !== "undefined") {
        if (localStorage.hash && localStorage.hash !== '') {
            hashToLoad = window.localStorage.hash;
            delete window.localStorage.hash;
        }

    } else{
        hashToLoad = loadUserData('hash',true);
    }
    return hashToLoad;
}

/*
 * loadUserData is een functie voor het raadplegen van gegevens in internet explorer m.b.v. userData.
 * Zie: http://msdn.microsoft.com/en-us/library/ms531424(v=vs.85).aspx
 */
function loadUserData(key,remove) {
    var bdUserData = document.getElementById("bdUserData");
    var dataToLoad ='';
    if (bdUserData.addBehavior) {
        bdUserData.load("bdDataStorage");
        if (bdUserData.getAttribute(key)) {
            dataToLoad = bdUserData.getAttribute(key);
            if (remove){
                bdUserData.removeAttribute(key);
            }
            bdUserData.save("bdDataStorage");
        }
    }
    return dataToLoad;
}

/*
 * saveUserData is een functie voor het opslaan van gegevens in internet explorer m.b.v. userData.
 * Zie: http://msdn.microsoft.com/en-us/library/ms531424(v=vs.85).aspx
 */
function saveUserData(key,value) {
    var bdUserData = document.getElementById("bdUserData");
    if (bdUserData.addBehavior) {
        bdUserData.load("bdDataStorage");
        var oTimeNow        = new Date(); // Start Time
        oTimeNow.setHours(oTimeNow.getHours() + 24);
        var sExpirationDate = oTimeNow.toUTCString();
        bdUserData.expires  = sExpirationDate;
        bdUserData.setAttribute(key,value);
        bdUserData.save("bdDataStorage");
    }
}

