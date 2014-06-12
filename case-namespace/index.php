<?php

require_once "vendor/autoload.php";

use Ilpaijin\Monitor;

// $monitor = new Monitor();

// $cfg = array("primo","secondo");


var_dump(php_sapi_name());

var_dump(__DIR__);

var_dump(dirname(__DIR__));

var_dump($_SERVER['REQUEST_URI']);

var_dump(is_file(__DIR__ . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH)));

// $monitor->printMed("string");

// var_dump($monitor);