/**
 * Created by root on 3/26/15.
 */

  $(function() {
    // run the currently selected effect
    function runEffect() {
      // get effect type from
      var selectedEffect = "fold";

      // most effect types need no options passed by default
      var options = {};
      // some effects have required parameters
      if ( selectedEffect === "scale" ) {
        options = { percent: 0 };
      } else if ( selectedEffect === "size" ) {
        options = { to: { width: 200, height: 60 } };
      }

      // run the effect
      //$( "#tabs" ).hide( selectedEffect, options, 1000, callback );
        $( "#tabs" ).hide( selectedEffect, options, 1000 );
    };

    // callback function to bring a hidden box back
    function callback() {
      setTimeout(function() {

        $( "#tabs" ).removeAttr( "style" ).hide().fadeIn();
      }, 1000 );

    };

    // set effect from select menu value
    $( "#button" ).click(function() {
      runEffect();
    });
      $( "#menubutton" ).click(function() {
      callback();
    });
  });
