<?php

function get_diagnosis($test){//En entrée, le fichier sous forme de chaîne de caractères
  $data = array("content"=>$test);
  $postdata = http_build_query($data); 
  $opts = array('http' =>
    array(
        'method'  => 'POST',
        'header'  => 'Content-type: application/x-www-form-urlencoded',
        'content' => $postdata
      )
    );
  $context  = stream_context_create($opts);
  $url = "https://daniel.greyc.fr/public/index.php?a=TestDAnIEL";
  $result = file_get_contents($url, false, $context);
  if(strpos($result,"as relevant for")){
    $diagnosis = "Relevant";
  }
  else{
    $diagnosis = "Irrelevant";
  }
  return $diagnosis;//En sortie, un diagnostic sur la classe du document
  }
$test = "<p>Some content in a paragraph Grippe</p><p>Another Grippe paragraph with other content</p>";
echo get_diagnosis($test)."\n";
?>
