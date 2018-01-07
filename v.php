<?php
    session_start();
    
    if(isset($_SESSION["cool2"]))
    {
        
    }else{
        exit();
    }
?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">

    <title>Carpool</title>

    <!-- Bootstrap core CSS -->
    <link href="../../dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <link href="../../assets/css/ie10-viewport-bug-workaround.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="signin.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="../../assets/js/ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
      <style>
       #map {
        height: 400px;
        width: 100%;
       }
    </style>

  </head>

  <body>
       <h2 class="form-signin-heading">Details</h2>
      <input type="text" name="areaname"><button  name="search" onclick="find()" >Search</button>
      <div id="map"></div>
    <div class="container">

      <form class="form-signin" method="post" action="index.php">
          

        <label for="timings" class="sr-only">Where:</label>
        <input type="hidden" id="dest" name="dest" value="">
          <div>
            
            <script>
				var directionsDisplay = new google.maps.DirectionsRenderer();
                var directionsService = new google.maps.DirectionsService();
				var map = new google.maps.Map(document.getElementById('map'), {
                        zoom: 20,
                        center: habib
                    });
				var bounds = new google.maps.LatLngBounds();
                function initMap() {
                    
                    
                    var habib = { lat: 24.9053, lng: 67.1377 };
                    var markerslist = [habib]
                    
                    var dest = { lat: 0, lng: 0 };
                    var marker = [new google.maps.Marker({
                        position: habib,
                        map: map
                    })];
                    
                    map.addListener('click', function (e) {
                        dest = e.latLng;
						var tmp=markerslist.pop();
                        markerslist.push(dest);
                        document.getElementById("markers").value = JSON.stringify(markerslist);
                        bounds.extend(habib);
                        bounds.extend(dest);
                        map.fitBounds(bounds);
						marker.pop().setMap(null);
                        marker.push(new google.maps.Marker({ position: dest, map: map }));
                        var request = {
                            origin: habib,
                            destination: dest,
                            travelMode: google.maps.TravelMode.DRIVING
                        };
                        directionsService.route(request, function (response, status) {
                            if (status == google.maps.DirectionsStatus.OK) {
                                directionsDisplay.setDirections(response);
                                directionsDisplay.setMap(map);
                            } else {
                                alert("Directions Request from " + start.toUrlValue(6) + " to " + end.toUrlValue(6) + " failed: " + status);
                            }
                        });
                    });
                    
                }
            </script>
            <script async defer
            src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDeue4OVkVkVB5IvDQMsslDBJ-L3WKTesI&callback=initMap">
            </script>

        </div>
        <button class="btn btn-lg btn-primary btn-block" name="v23" type="submit">Next</button>
      </form>
        
    </div> <!-- /container -->


    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>