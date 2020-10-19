import { shallowMount } from "@vue/test-utils";
import App from "@/App";

describe("App", () => {
  it("renders the component", () => {
    const wrapper = shallowMount(App);

    expect(wrapper.html()).toMatchSnapshot();
  });
});
