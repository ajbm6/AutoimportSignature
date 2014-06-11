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

    /**
     * @link /PHP/Sublime_Text_2-autoimport_signature/case-namespace/src/Ilpaijin/Interfaces/PrintableInterface.php
     * @see Interfaces\PrintableInterface
     */
    public function printMe ($a, $b)
    {
        //Do something
    }
            
    // ***WARNING*** Method "printYou" already declared
            
    /**
     * @link /PHP/Sublime_Text_2-autoimport_signature/case-namespace/src/Ilpaijin/Interfaces/PrintableInterface.php
     * @see Interfaces\PrintableInterface
     */
    public function printHe ($a, $b)
    {
        //Do something
    }
            
    function __construct()
    {
        $this->printMe();

    }

    public function printMed($param)
    {
        if(!is_array($param) && !is_object($param))
        {
            throw new \InvalidArgumentException(printf(" You can't pass parameter with format %s", gettype($param)));
        }

        $this->param = $param;
    }

    public function printYou($who)
    {

    }

    public function printHey()
    {
        # code...
    }

}