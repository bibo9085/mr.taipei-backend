<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateMrtsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('mrts', function (Blueprint $table) {
            $table->id('mrt_id');
            $table->string('mrt_name',20);
            $table->float('mrt_longitude');
            $table->float('mrt_latitude');
            $table->string('mrt_number',50);
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('mrts');
    }
}
