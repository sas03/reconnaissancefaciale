<!DOCTYPE html>
<html>
<head>
<style>
#container {
	margin: 0px auto;
	width: 500px;
	height: 355px;
	border: 10px #333 solid;
  border-radius: 20px;
}
#videoElement {
	width: 500px;
	height: 375px;
	background-color: #666;
}
li{
  display: inline;
  font-weight: bold;
  font-size: 20px;
}
</style>
<script>
function myFunction() {
  document.getElementById("demo").innerHTML = "Click on the right button to start";
}
</script>
</head>
 <hr>
<body style="background-color: gray; background-image: url('reco.jpg'); background-repeat: no-repeat; background-size: 100% 1000px;">
<nav style="background-color: gray; margin: 10px; padding: 10px; border: 5px solid black; border-radius: 10px">
  <ul style="text-align: center; list-style-type: none">
    <li><a href="index.php">Home</a></li>
    <li><a href="about.php">About</a></li>
    <li><a href="member.php">Members</a></li>
  </ul>
</nav>
<hr>
<h1 style='text-align: center;'>Reconnaissance Faciale</h1>
<div id="container" style="margin-bottom: 5px; background-color: gray; text-align: center">
	<img src="https://saelectronics.co.za/index_htm_files/animated-cameras.gif"/>
</div>
<div style="text-align: center">
	<button type="button" onclick="myFunction()">Explanation</button>
	<a href="index.php?camera=1"><button>Facial recognition</button></a>
  <?php
    if (isset($_GET["camera"])){
            //$command = escapeshellcmd('.\..\scripts\firstAlgo.py');
            $command = escapeshellcmd('detect.py');
            $output = utf8_encode(shell_exec($command));
            echo "<p style='font-weight: bold; color: white'>Camera recognition started</p>";
            echo " <p>".$output."</p>";

            ini_set('max_execution_time', 300); //300 seconds = 5 minutes
            set_time_limit(300);
    }
  ?>

</div>
<div style="background-color: gray; margin: 0 auto; width: 250px">
  <p id="demo" style="text-align: center; color: white; font-weight: bold;">Description</p>
</div>

<hr style="margin-top: 12%">
<p style="text-align: center; font-weight: bold; font-size: 20px; background-color: gray; margin: 10px; padding: 25px; border: 5px solid black; border-radius: 10px">Signature - Copyright@SSA2020</p>
