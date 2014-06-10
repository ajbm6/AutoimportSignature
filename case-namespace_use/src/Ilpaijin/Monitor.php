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
    /**
     * @link /PHP/Sublime_Text_2-autoimport_signature/case-namespace_use/src/Ilpaijin/Interfaces/PrintableInterface.php
     * @see Interfaces\PrintableInterface
     */
    public function printMe()
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