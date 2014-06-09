<?php

namespace Ilpaijin;

use Ilpaijin\Interfaces\PrintableInterface as IPrintable;

/**
* Monitor Description
*
* @author ilpaijin <ilpaijin@gmail.com>
*/
class Monitor implements IPrintable
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