<?php

namespace Ilpaijin;

/**
* Monitor Description
*
* @author ilpaijin <ilpaijin@gmail.com>
*/
class Monitor implements React\Promise\PromisorInterface
{
    function __construct()
    {
        $this->printMe();
        $this->saveMe();
        $this->holdMe;
    }

    public function printMe()
    {

    }

    public function saveMe()
    {

    }

    public function holdMe()
    {
        # code...
    }

}