<?php

require_once "vendor/autoload.php";

use Ilpaijin\Monitor;

$monitor = new Monitor();

$cfg = array("primo","secondo");

$monitor->printMed("string");

var_dump($monitor);