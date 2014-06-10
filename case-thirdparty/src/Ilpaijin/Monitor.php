<?php

namespace Ilpaijin;

/**
* Monitor Description
*
* @author ilpaijin <ilpaijin@gmail.com>
*/
class Monitor implements React\Promise\PromisorInterface
{
    /**
     * @link /PHP/Sublime_Text_2-autoimport_signature/case-thirdparty/src/Ilpaijin/React/Promise/PromisorInterface.php
     * @see React\Promise\PromisorInterface
     */
    public function promise()
    {
        //Do something
    }
            
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