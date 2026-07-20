module timing_generator (
    input wire enable, clk, rst_n,
    output wire hsync, vsync, video_active,
    output reg signed [10:0] x_t, y_t
);
    reg active;

    always @(posedge clk) begin
        if (~rst_n) begin
            active <= 0;
            x_t <= -32;
            y_t <= 0;
        end
        else begin
            if (active) begin
                if (x_t == 799) begin
                    x_t <= 0;
                    if (y_t == 524) begin
                        y_t <= 0;
                    end
                    else begin
                        y_t <= y_t + 1;
                    end
                end
                else begin
                    x_t <= x_t + 1;
                end
            end
            else begin
                if (enable) begin
                    active <= 1;
                    x_t <= 0;
                    y_t <= 0;
                end
            end
        end
    end

    assign hsync = !((656 <= x_t) && (751 >= x_t));
    assign vsync = !((490 <= y_t) && (491 >= y_t));
    assign video_active = (639 >= x_t) && (479 >= y_t) && (0 <= x_t) && (0 <= y_t);

endmodule