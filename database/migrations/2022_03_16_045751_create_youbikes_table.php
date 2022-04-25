<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateYoubikesTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('youbikes', function (Blueprint $table) {
            $table->id('yb_id');
            $table->string('yb_name',20);
            $table->string('yb_place',20);
            $table->float('yb_longitude');
            $table->float('yb_latitude');
            $table->integer('yb_number');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('youbikes');
    }
}
