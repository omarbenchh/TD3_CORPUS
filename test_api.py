import requests

def get_diagnosis(test):
  url = "https://daniel.greyc.fr/public/index.php?a=TestDAnIEL"
  r = requests.post(url, data = {"content":test})
  result = r.text
  if "as relevant for" in result:
    diagnosis = "Relevant"
  else:
    diagnosis = "Irrelevant"
  return diagnosis
#  $postdata = http_build_query($data); 
#  $opts = array('http' =>
#    array(
#        'method'  => 'POST',
#        'header'  => 'Content-type: application/x-www-form-urlencoded',
#        'content' => $postdata
#      )
#    );
#  $context  = stream_context_create($opts);
#  $result = file_get_contents($url, false, $context);
#    $diagnosis = "Relevant";
#  }
test_relevant = "<p>Some content in a paragraph Grippe</p><p>Another Grippe paragraph with other content</p>"
test_irrelevant = "<p>Some content in a paragraph </p><p>Another paragraph with other content</p>"

print get_diagnosis(test_relevant)
