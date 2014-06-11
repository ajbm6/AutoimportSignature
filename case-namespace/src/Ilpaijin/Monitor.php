<?php

namespace Ilpaijin;

/**
* Monitor Description
*
* @author ilpaijin <ilpaijin@gmail.com>
*/
class Monitor implements Interfaces\PrintableInterface 
{
    public $params;

    function __construct()
    {
        $this->printMe();

    }

    public function printMed($param)
    {
        if(!is_array($param) || !is_object($param))
        {
            throw new InvalidArgumentException(printf(" You can't pass parameter with format %s", gettype($param)));
        }

        $this->params = $params;

    }

    public function printYou($whos)
    {
        //Do something
    }

    public function printHey()
    {
        # code...
    }

}